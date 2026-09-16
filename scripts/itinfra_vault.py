#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
itinfra_vault.py — Local Encrypted Secret Vault (AES-256-GCM) per ItInfra.

Caratteristiche:
- Cifratura autenticata simmetrica AES-256-GCM (12-byte nonce, 16-byte auth tag).
- Derivazione chiave crittografica PBKDF2-HMAC-SHA256 (100.000 iterazioni, 16-byte salt casuale).
- File Locking atomico (.vault.lock) con context manager per prevenire race conditions in multi-worktree.
- Risoluzione dinamica della root repo per operare correttamente all'interno di Git Worktrees.
- Audit di consistenza dei puntatori vault:// presenti nei documenti Markdown di progetto.
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    HAVE_CRYPTO = True
except ImportError:
    HAVE_CRYPTO = False


class VaultError(Exception):
    """Eccezione base per gli errori del Vault."""
    pass


class FileLock:
    """
    Lock atomico cross-platform basato su file system (.vault.lock).
    Garantisce l'accesso esclusivo al vault tra processi o agenti in parallelo.
    """
    def __init__(self, lock_path: Path, timeout: float = 10.0, poll_interval: float = 0.1):
        self.lock_path = lock_path
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.fd: Optional[int] = None

    def acquire(self) -> bool:
        start_time = time.time()
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)

        while True:
            try:
                # O_CREAT | O_EXCL assicura atomicita' sia su Windows che Unix
                self.fd = os.open(
                    str(self.lock_path),
                    os.O_CREAT | os.O_EXCL | os.O_RDWR
                )
                info = f"pid={os.getpid()} time={datetime.now(timezone.utc).isoformat()}\n"
                os.write(self.fd, info.encode("utf-8"))
                return True
            except FileExistsError:
                # Controlla se il lock e' obsoleto (stale lock > 120s)
                try:
                    mtime = os.path.getmtime(self.lock_path)
                    if time.time() - mtime > 120:
                        try:
                            os.remove(self.lock_path)
                            continue
                        except OSError:
                            pass
                except OSError:
                    pass

                if time.time() - start_time >= self.timeout:
                    raise VaultError(
                        f"Timeout ({self.timeout}s) acquisizione lock su {self.lock_path}. "
                        "Un altro agente o processo sta modificando il vault."
                    )
                time.sleep(self.poll_interval)

    def release(self):
        if self.fd is not None:
            try:
                os.close(self.fd)
            except OSError:
                pass
            self.fd = None
        if self.lock_path.exists():
            try:
                os.remove(self.lock_path)
            except OSError:
                pass

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class VaultManager:
    """
    Gestore del Local Encrypted Vault per uno specifico progetto IT.
    """
    def __init__(self, project_slug: str, repo_root: Optional[Path] = None):
        self.slug = project_slug
        self.repo_root = repo_root or self._find_repo_root()
        self.project_dir = self.repo_root / "projects" / self.slug
        self.vault_file = self.project_dir / ".vault.enc"
        self.lock_file = self.project_dir / ".vault.lock"

        if not HAVE_CRYPTO:
            raise VaultError(
                "La libreria Python 'cryptography' non è installata. "
                "Esegui: pip install cryptography"
            )

    @staticmethod
    def _find_repo_root() -> Path:
        """Determina la root del repository principale anche da dentro un Git Worktree."""
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True
            )
            return Path(res.stdout.strip())
        except (subprocess.SubprocessError, FileNotFoundError):
            return Path(__file__).resolve().parent.parent

    @staticmethod
    def _derive_key(passphrase: str, salt: bytes) -> bytes:
        """Deriva una chiave simmetrica a 256 bit con PBKDF2-HMAC-SHA256."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        return kdf.derive(passphrase.encode("utf-8"))

    def exists(self) -> bool:
        """Verifica se il file vault del progetto esiste."""
        return self.vault_file.is_file()

    def init_vault(self, passphrase: str, overwrite: bool = False) -> Path:
        """Inizializza un nuovo vault cifrato per il progetto."""
        if not passphrase:
            raise VaultError("La passphrase non può essere vuota.")

        if self.vault_file.exists() and not overwrite:
            raise VaultError(
                f"Il vault esiste già in {self.vault_file}. Usa overwrite=True per sovrascriverlo."
            )

        self.project_dir.mkdir(parents=True, exist_ok=True)
        with FileLock(self.lock_file):
            salt = os.urandom(16)
            key = self._derive_key(passphrase, salt)
            nonce = os.urandom(12)
            aesgcm = AESGCM(key)

            initial_data = {
                "_metadata": {
                    "project_slug": self.slug,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "version": "1.0"
                },
                "secrets": {}
            }
            plaintext = json.dumps(initial_data).encode("utf-8")
            ciphertext = aesgcm.encrypt(nonce, plaintext, None)

            envelope = {
                "version": "1.0",
                "cipher": "AES-256-GCM",
                "kdf": "PBKDF2-HMAC-SHA256",
                "iterations": 100000,
                "salt": salt.hex(),
                "nonce": nonce.hex(),
                "ciphertext": ciphertext.hex(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }

            temp_file = self.vault_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(envelope, f, indent=2)
            temp_file.replace(self.vault_file)

        return self.vault_file

    def _read_and_decrypt(self, passphrase: str) -> Dict[str, Any]:
        """Legge ed esegue la decifratura verificando il tag di autenticazione."""
        if not self.vault_file.exists():
            raise VaultError(f"Vault non trovato in {self.vault_file}. Esegui prima 'init'.")

        try:
            with open(self.vault_file, "r", encoding="utf-8") as f:
                envelope = json.load(f)
        except Exception as e:
            raise VaultError(f"Errore lettura file vault: {e}")

        try:
            salt = bytes.fromhex(envelope["salt"])
            nonce = bytes.fromhex(envelope["nonce"])
            ciphertext = bytes.fromhex(envelope["ciphertext"])
        except (KeyError, ValueError) as e:
            raise VaultError(f"Formato envelope vault corrotto: {e}")

        key = self._derive_key(passphrase, salt)
        aesgcm = AESGCM(key)

        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            return json.loads(plaintext.decode("utf-8"))
        except Exception:
            raise VaultError("Autenticazione o decifratura fallita: passphrase errata o vault corrotto.")

    def _encrypt_and_write(self, data: Dict[str, Any], passphrase: str):
        """Cifra e salva atomicamente i dati aggiornati."""
        salt = os.urandom(16)
        key = self._derive_key(passphrase, salt)
        nonce = os.urandom(12)
        aesgcm = AESGCM(key)

        plaintext = json.dumps(data).encode("utf-8")
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        envelope = {
            "version": "1.0",
            "cipher": "AES-256-GCM",
            "kdf": "PBKDF2-HMAC-SHA256",
            "iterations": 100000,
            "salt": salt.hex(),
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        temp_file = self.vault_file.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(envelope, f, indent=2)
        temp_file.replace(self.vault_file)

    def set_secret(self, key_path: str, secret_value: str, passphrase: str) -> None:
        """Salva o aggiorna un secret nel vault in modo atomico e concurrency-safe."""
        key_clean = key_path.strip().strip("/")
        if not key_clean:
            raise VaultError("La chiave del secret non può essere vuota.")

        with FileLock(self.lock_file):
            data = self._read_and_decrypt(passphrase)
            if "secrets" not in data:
                data["secrets"] = {}
            data["secrets"][key_clean] = {
                "value": secret_value,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            self._encrypt_and_write(data, passphrase)

    def get_secret(self, key_path: str, passphrase: str) -> Optional[str]:
        """Recupera il valore decifrato di un secret."""
        key_clean = key_path.strip().strip("/")
        with FileLock(self.lock_file):
            data = self._read_and_decrypt(passphrase)
            secret_entry = data.get("secrets", {}).get(key_clean)
            if isinstance(secret_entry, dict):
                return secret_entry.get("value")
            elif isinstance(secret_entry, str):
                return secret_entry
            return None

    def delete_secret(self, key_path: str, passphrase: str) -> bool:
        """Elimina un secret dal vault."""
        key_clean = key_path.strip().strip("/")
        with FileLock(self.lock_file):
            data = self._read_and_decrypt(passphrase)
            secrets = data.get("secrets", {})
            if key_clean in secrets:
                del secrets[key_clean]
                self._encrypt_and_write(data, passphrase)
                return True
            return False

    def list_keys(self, passphrase: str) -> List[Dict[str, str]]:
        """Elenca le chiavi memorizzate con relativo timestamp (senza mai esporre i secret in chiaro)."""
        with FileLock(self.lock_file):
            data = self._read_and_decrypt(passphrase)
            secrets = data.get("secrets", {})
            result = []
            for k in sorted(secrets.keys()):
                entry = secrets[k]
                upd = entry.get("updated_at", "N/A") if isinstance(entry, dict) else "N/A"
                result.append({"key": k, "updated_at": upd})
            return result

    def scan_markdown_references(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Scansiona tutti i file .md nella directory di progetto alla ricerca di puntatori vault://.
        Pattern supportati:
          vault://it/<project>/<key>
          vault://it/projects/<slug>/<key>
          vault://<key>
        """
        import re
        ref_pattern = re.compile(r'vault://(?:it/)?(?:projects/)?(?:[a-zA-Z0-9_\-]+/)?([a-zA-Z0-9_\-\.\/]+)')

        results = {}
        if not self.project_dir.exists():
            return results

        for md_file in sorted(self.project_dir.glob("*.md")):
            try:
                content = md_file.read_text(encoding="utf-8")
            except Exception:
                continue

            found = []
            for line_no, line in enumerate(content.splitlines(), start=1):
                for match in ref_pattern.finditer(line):
                    raw_uri = match.group(0)
                    key = match.group(1).strip("/")
                    found.append({
                        "line": line_no,
                        "raw_uri": raw_uri,
                        "key": key
                    })
            if found:
                results[md_file.name] = found
        return results

    def audit_references(self, passphrase: Optional[str] = None) -> Dict[str, Any]:
        """
        Esegue l'audit dei riferimenti vault:// rispetto alle chiavi censite nel vault cifrato.
        """
        scanned = self.scan_markdown_references()
        all_referenced_keys = set()
        for refs in scanned.values():
            for r in refs:
                all_referenced_keys.add(r["key"])

        vault_keys = None
        missing_in_vault = []
        unused_in_vault = []

        if passphrase and self.exists():
            try:
                keys_meta = self.list_keys(passphrase)
                vault_keys = set(k["key"] for k in keys_meta)
                missing_in_vault = sorted(list(all_referenced_keys - vault_keys))
                unused_in_vault = sorted(list(vault_keys - all_referenced_keys))
            except Exception as e:
                return {
                    "error": f"Impossibile decifrare il vault per l'audit: {e}",
                    "scanned_references": scanned,
                    "referenced_keys": sorted(list(all_referenced_keys))
                }

        return {
            "project_slug": self.slug,
            "vault_exists": self.exists(),
            "vault_file": str(self.vault_file),
            "files_with_references": len(scanned),
            "total_references_count": sum(len(v) for v in scanned.values()),
            "referenced_keys": sorted(list(all_referenced_keys)),
            "vault_keys": sorted(list(vault_keys)) if vault_keys is not None else None,
            "missing_in_vault": missing_in_vault,
            "unused_in_vault": unused_in_vault,
            "scanned_details": scanned
        }

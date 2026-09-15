/**
 * ============================================================================
 * itInfrastructureService.ts
 * ============================================================================
 *
 * Servizio backend per la compilazione di template documentali IT tramite
 * Gemini 3.7 Flash. Delega la logica di prompt construction e chiamata AI
 * al modello generativo, garantendo output conforme a OKF v0.2.
 *
 * Da collocare in: server/services/itInfrastructureService.ts
 *
 * Dipendenze:
 * - @google/genai (già presente nel Knowledge Vault)
 * - Tipi ITDocType da ../src/types (richiede Livello 2 applicato)
 * - IT_DOC_TYPES, getITBoilerplate da ../src/lib/okfItTemplates (Livello 2)
 *
 * ============================================================================
 */

import { GoogleGenAI, Type } from "@google/genai";
import { IT_DOC_TYPES, getITBoilerplate } from "../src/lib/okfItTemplates";
import { ITDocType } from "../src/types";
import * as dotenv from "dotenv";

dotenv.config();

const GEMINI_API_KEY = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || "";
const GEMINI_MODEL = process.env.GEMINI_MODEL || "gemini-2.5-flash";

/**
 * Contesto per la compilazione del template IT.
 */
export interface ITTemplateCompileContext {
  docType: string;
  docTypeInfo: {
    canonical: "specification" | "architecture" | "guide";
    label: string;
    phase: 1 | 2 | 3 | 4 | 5 | 6 | 7;
    description: string;
  };
  boilerplate: string;             // YAML boilerplate con placeholder già sostituiti
  project: {
    id: string;
    name: string;
    site?: string;
    customer?: string;
    author?: string;
    reviewer?: string;
    approver?: string;
    owner_team?: string;
  };
  customData?: string;               // textarea libera con dati specifici
}

export interface ITTemplateCompileResult {
  success: boolean;
  markdown?: string;
  error?: string;
  modelUsed?: string;
  durationMs?: number;
}

/**
 * Client Gemini (singleton).
 */
let _geminiClient: GoogleGenAI | null = null;

function getGeminiClient(): GoogleGenAI {
  if (!_geminiClient) {
    if (!GEMINI_API_KEY) {
      throw new Error("GEMINI_API_KEY (o GOOGLE_API_KEY) non configurata nelle variabili ambiente");
    }
    _geminiClient = new GoogleGenAI({ apiKey: GEMINI_API_KEY });
  }
  return _geminiClient;
}

/**
 * Costruisce il system prompt per Gemini che definisce il comportamento atteso.
 */
function buildSystemPrompt(ctx: ITTemplateCompileContext): string {
  return `Sei un System Engineer senior specializzato in infrastrutture IT enterprise.
Il tuo compito è compilare un template documentale del ciclo lavorativo IT, 
restituendo un documento Markdown completo conforme allo standard OKF v0.2 (Open Knowledge Format).

REGOLE FONDAMENTALI:
1. Il documento DEVE iniziare con un blocco YAML frontmatter delimitato da --- ... ---
2. Lo YAML DEVE contenere: okf_version: "0.2", id, title, type, domain, tags, entities, relations
3. Il campo type DEVE essere il tipo canonico OKF: "${ctx.docTypeInfo.canonical}"
4. Il documento DEVE includere anche i metadati IT estesi (project_id, phase, related_docs, depends_on, ecc.)
5. NON inventare dati tecnici (IP, seriali, MAC) se non forniti: usa "<DA-RICHIEDERE>" e segnala in "Open Issues"
6. Sostituisci TUTTI i placeholder <...> con valori reali o <DA-RICHIEDERE>
7. NON inserire password in chiaro: usa riferimenti al vault (es. vault://it/<project>/fw-01/admin)
8. Lingua: italiano per body e sezioni, inglese per termini tecnici standard (HLD, LLD, VLAN, ecc.)
9. Mantieni la struttura del boilerplate YAML, espandendo il body Markdown con sezioni appropriate
10. Per ogni ID presente in related_docs, deve esistere una corrispondente entry in relations con targetId uguale
11. Non usare emoji nel documento
12. Non aggiungere conclusioni artificiali o marker di fine documento

OUTPUT FORMAT:
Restituisci SOLO il documento Markdown completo, senza testo aggiuntivo, commenti o spiegazioni.
Il documento deve iniziare con --- (frontmatter YAML) e terminare con l'ultima sezione di contenuto.`;
}

/**
 * Costruisce il prompt utente con i dati concreti.
 */
function buildUserPrompt(ctx: ITTemplateCompileContext): string {
  const projectLines = [
    `project_id: ${ctx.project.id}`,
    `project_name: ${ctx.project.name}`,
  ];
  if (ctx.project.site) projectLines.push(`site: ${ctx.project.site}`);
  if (ctx.project.customer) projectLines.push(`customer: ${ctx.project.customer}`);
  if (ctx.project.author) projectLines.push(`author: ${ctx.project.author}`);
  if (ctx.project.reviewer) projectLines.push(`reviewer: ${ctx.project.reviewer}`);
  if (ctx.project.approver) projectLines.push(`approver: ${ctx.project.approver}`);
  if (ctx.project.owner_team) projectLines.push(`owner_team: ${ctx.project.owner_team}`);

  return `Compila il seguente template documentale IT:

TIPO DOCUMENTO: ${ctx.docType} (${ctx.docTypeInfo.label})
FASE: ${ctx.docTypeInfo.phase}
TIPO CANONICO OKF: ${ctx.docTypeInfo.canonical}
DESCRIZIONE TIPO: ${ctx.docTypeInfo.description}

DATI PROGETTO:
${projectLines.join("\n")}

${ctx.customData ? `DATI SPECIFICI DEL DOCUMENTO:
${ctx.customData}

` : ""}BOILERPLATE YAML DI PARTENZA (da completare con i dati sopra):
\`\`\`yaml
${ctx.boilerplate}
\`\`\`

ISTRUZIONI:
1. Mantieni la struttura del boilerplate YAML, espandendo i campi con i valori forniti
2. Genera il body Markdown completo con tutte le sezioni appropriate per il tipo ${ctx.docType}
3. Sostituisci i placeholder <...> con valori reali o <DA-RICHIEDERE>
4. Aggiungi almeno 3-5 entità significative nel blocco entities
5. Mantieni le relations dal boilerplate, aggiungendone altre se logico
6. Rispetta le AI-INSTRUCTIONS del template (zero invenzioni, coerenza, no secret in chiaro)

Restituisci SOLO il documento Markdown completo.`;
}

/**
 * Compila un template IT chiamando Gemini 3.7 Flash.
 */
export async function compileITTemplate(
  ctx: ITTemplateCompileContext
): Promise<ITTemplateCompileResult> {
  const startTime = Date.now();

  try {
    const client = getGeminiClient();
    const systemPrompt = buildSystemPrompt(ctx);
    const userPrompt = buildUserPrompt(ctx);

    console.log(`[IT Infrastructure] Compiling template: ${ctx.docType} for project ${ctx.project.id}`);

    const response = await client.models.generateContent({
      model: GEMINI_MODEL,
      contents: userPrompt,
      config: {
        systemInstruction: systemPrompt,
        temperature: 0.3,        // bassa temperatura per output deterministico
        maxOutputTokens: 8192,
        responseMimeType: "text/plain",
      },
    });

    const markdown = response.text || "";

    if (!markdown || markdown.trim().length < 100) {
      return {
        success: false,
        error: "Output Gemini vuoto o troppo corto",
        modelUsed: GEMINI_MODEL,
        durationMs: Date.now() - startTime,
      };
    }

    // Verifica che inizi con --- (frontmatter)
    if (!markdown.trim().startsWith("---")) {
      return {
        success: false,
        error: "Output non inizia con frontmatter YAML ---",
        modelUsed: GEMINI_MODEL,
        durationMs: Date.now() - startTime,
      };
    }

    return {
      success: true,
      markdown: markdown.trim(),
      modelUsed: GEMINI_MODEL,
      durationMs: Date.now() - startTime,
    };
  } catch (err: any) {
    console.error("[IT Infrastructure] Errore compilazione template:", err);
    return {
      success: false,
      error: err?.message || "Errore sconosciuto durante la chiamata a Gemini",
      modelUsed: GEMINI_MODEL,
      durationMs: Date.now() - startTime,
    };
  }
}

/**
 * Health check del servizio (utile per monitoraggio).
 */
export async function checkITServiceHealth(): Promise<{
  status: "ok" | "error";
  geminiConfigured: boolean;
  model: string;
  error?: string;
}> {
  if (!GEMINI_API_KEY) {
    return {
      status: "error",
      geminiConfigured: false,
      model: GEMINI_MODEL,
      error: "GEMINI_API_KEY non configurata",
    };
  }
  return {
    status: "ok",
    geminiConfigured: true,
    model: GEMINI_MODEL,
  };
}

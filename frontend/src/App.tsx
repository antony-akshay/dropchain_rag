import { useRef, useState } from "react";
import { queryDocument, uploadDocument } from "./api";

type Message = {
  role: "system" | "user" | "assistant";
  content: string;
  citations?: string[];
};

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [documentName, setDocumentName] = useState("");
  const [openCitation, setOpenCitation] = useState<number | null>(null);

  const fileRef = useRef<HTMLInputElement>(null);

  const handleUpload = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = e.target.files?.[0];

    if (!file) return;

    try {
      const result = await uploadDocument(file);

      setDocumentName(file.name);

      setMessages((prev) => [
        ...prev,
        {
          role: "system",
          content: `📄 ${file.name} uploaded successfully (${result.chunks} chunks indexed)`,
        },
      ]);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const result = await queryDocument(userQuestion);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: result.answer,
          citations: result.sources,
        },
      ]);
    } catch (error: any) {
      console.error("FULL ERROR:", error);
      console.error("RESPONSE:", error?.response);
      console.error("DATA:", error?.response?.data);

      alert(JSON.stringify(error?.response?.data ?? error.message, null, 2));
    } finally {
      setLoading(false);
    }
  };

  const clearContext = () => {
    setMessages([]);
    setDocumentName("");
    setOpenCitation(null);
  };

  return (
    <div className="h-screen flex flex-col bg-zinc-950 text-zinc-100">
      {/* Header */}

      <header className="border-b border-zinc-800 px-6 py-4 flex items-center justify-between">
        <h1 className="font-semibold text-lg">
          Mini Contextual AI Assistant
        </h1>

        <div className="flex gap-3">
          <button
            onClick={() => fileRef.current?.click()}
            className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-sm"
          >
            Upload Document
          </button>

          <button
            onClick={clearContext}
            className="px-4 py-2 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-sm"
          >
            Clear Context
          </button>
        </div>

        <input
          ref={fileRef}
          type="file"
          accept=".txt"
          hidden
          onChange={handleUpload}
        />
      </header>

      {/* Chat */}

      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-8">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center mt-32">
              <h2 className="text-2xl font-semibold mb-3">
                Upload a document to begin
              </h2>

              <p className="text-zinc-400">
                Ask questions about the uploaded knowledge base.
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index} className="mb-6">
              {/* User */}

              {message.role === "user" && (
                <div className="flex justify-end">
                  <div className="max-w-2xl bg-emerald-600 text-white px-4 py-3 rounded-2xl">
                    {message.content}
                  </div>
                </div>
              )}

              {/* Assistant */}

              {message.role === "assistant" && (
                <div className="flex justify-start">
                  <div className="max-w-3xl">
                    <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4">
                      {message.content}
                    </div>

                    {message.citations && !message.citations.includes("I don't know based on the provided document.") &&
                      message.citations.length > 0 && (
                        <div className="mt-2">
                          <button
                            onClick={() =>
                              setOpenCitation(
                                openCitation === index
                                  ? null
                                  : index
                              )
                            }
                            className="text-xs text-emerald-400 hover:text-emerald-300"
                          >
                            {openCitation === index
                              ? "Hide Sources ▲"
                              : "Show Sources ▼"}
                          </button>

                          {openCitation === index && (
                            <div className="mt-3 rounded-xl border border-zinc-800 bg-zinc-900 p-4">
                              <h4 className="text-sm font-medium text-emerald-400 mb-3">
                                Retrieved Chunks
                              </h4>

                              <div className="space-y-3">
                                {message.citations.map(
                                  (chunk, chunkIndex) => (
                                    <div
                                      key={chunkIndex}
                                      className="rounded-lg bg-zinc-950 border border-zinc-800 p-3 text-sm text-zinc-300 whitespace-pre-wrap"
                                    >
                                      {chunk}
                                    </div>
                                  )
                                )}
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                  </div>
                </div>
              )}

              {/* Uploaded Document */}

              {message.role === "system" && (
                <div className="flex justify-center">
                  <div className="bg-zinc-900 border border-emerald-500/30 text-emerald-300 text-sm rounded-xl px-4 py-3">
                    {message.content}
                  </div>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-4">
                Thinking...
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Composer */}

      <footer className="border-t border-zinc-800 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <input
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleAsk();
                }
              }}
              disabled={!documentName}
              placeholder={
                documentName
                  ? "Ask a question about the document..."
                  : "Upload a document first..."
              }
              className="flex-1 rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 outline-none focus:border-emerald-500"
            />

            <button
              onClick={handleAsk}
              disabled={!documentName || loading}
              className="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50"
            >
              Send
            </button>
          </div>

          {documentName && (
            <p className="text-xs text-zinc-500 mt-2">
              Active document: {documentName}
            </p>
          )}
        </div>
      </footer>
    </div>
  );
}
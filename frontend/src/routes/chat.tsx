import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send, Sparkles } from "lucide-react";

export const Route = createFileRoute("/chat")({
  head: () => ({
    meta: [
      { title: "AI Assistant — NeuroBudget" },
      { name: "description", content: "Chat with your AI finance assistant about budgets, goals and spending." },
    ],
  }),
  component: ChatPage,
});

type Msg = { role: "user" | "assistant"; content: string };

const SUGGESTIONS = [
  "How can I save more this month?",
  "Summarize my spending for August",
  "Am I on track for my vacation goal?",
];

function fakeReply(input: string) {
  if (/save|saving/i.test(input)) return "Based on your last 30 days, cutting dining out by 2 meals/week would save about $95. Want me to set a soft cap?";
  if (/spending|summary/i.test(input)) return "August so far: $2,500 spent. Top categories: Rent ($1,200), Groceries ($420), Entertainment ($240). You're at 83% of your $3,000 budget.";
  if (/goal|vacation/i.test(input)) return "Your Vacation Fund is at $1,820 / $3,000 (61%). At your current $260/mo pace you'll hit it in ~5 months.";
  return "Got it — I'll dig into your transactions and get back with a few concrete suggestions.";
}

function ChatPage() {
  const [messages, setMessages] = useState<Msg[]>([
    { role: "assistant", content: "Hi! I'm your NeuroBudget assistant. Ask me anything about your finances." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => { inputRef.current?.focus(); }, []);
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, loading]);

  const send = (text: string) => {
    const t = text.trim();
    if (!t || loading) return;
    setMessages((m) => [...m, { role: "user", content: t }]);
    setInput("");
    setLoading(true);
    setTimeout(() => {
      setMessages((m) => [...m, { role: "assistant", content: fakeReply(t) }]);
      setLoading(false);
      inputRef.current?.focus();
    }, 700);
  };

  return (
    <div className="mx-auto flex h-[calc(100vh-3.5rem)] max-w-3xl flex-col p-4">
      <div className="mb-3 flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <Sparkles className="h-4 w-4" />
        </div>
        <div>
          <h1 className="text-lg font-semibold leading-tight">AI Assistant</h1>
          <p className="text-xs text-muted-foreground">Personalized financial guidance</p>
        </div>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto rounded-2xl border bg-card p-4 shadow-[var(--shadow-soft)]">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            {m.role === "assistant" ? (
              <div className="max-w-[85%] text-sm leading-relaxed text-foreground">{m.content}</div>
            ) : (
              <div className="max-w-[80%] rounded-2xl bg-primary px-4 py-2 text-sm text-primary-foreground shadow-sm">
                {m.content}
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex gap-1 text-muted-foreground">
            <span className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/60" />
            <span className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/60 [animation-delay:120ms]" />
            <span className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/60 [animation-delay:240ms]" />
          </div>
        )}
        <div ref={endRef} />
      </div>

      {messages.length <= 1 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => send(s)}
              className="rounded-full border bg-background px-3 py-1.5 text-xs text-muted-foreground transition hover:bg-accent hover:text-accent-foreground"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      <Card className="mt-3 flex items-end gap-2 border-border/60 p-2 shadow-[var(--shadow-soft)]">
        <Textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              send(input);
            }
          }}
          placeholder="Ask about your spending, budgets, goals…"
          rows={1}
          className="min-h-[44px] resize-none border-0 bg-transparent shadow-none focus-visible:ring-0"
        />
        <Button size="icon" onClick={() => send(input)} disabled={!input.trim() || loading}>
          <Send className="h-4 w-4" />
        </Button>
      </Card>
    </div>
  );
}

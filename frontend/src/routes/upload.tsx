import { createFileRoute } from "@tanstack/react-router";
import { useRef, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Upload, FileText, CheckCircle2 } from "lucide-react";

export const Route = createFileRoute("/upload")({
  head: () => ({
    meta: [
      { title: "Upload Statements — NeuroBudget" },
      { name: "description", content: "Upload your CSV or PDF bank statements for AI-powered analysis." },
    ],
  }),
  component: UploadPage,
});

function UploadPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [drag, setDrag] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const onFiles = (list: FileList | null) => {
    if (!list) return;
    setFiles((f) => [...f, ...Array.from(list)]);
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Upload Statements</h1>
        <p className="text-sm text-muted-foreground">Drop CSV or PDF bank statements — we'll categorize them automatically.</p>
      </div>

      <Card className="shadow-[var(--shadow-soft)]">
        <CardContent className="p-6">
          <div
            onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
            onDragLeave={() => setDrag(false)}
            onDrop={(e) => { e.preventDefault(); setDrag(false); onFiles(e.dataTransfer.files); }}
            onClick={() => inputRef.current?.click()}
            className={`flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed p-12 text-center transition ${
              drag ? "border-primary bg-primary-soft" : "border-border hover:border-primary/60 hover:bg-accent/30"
            }`}
          >
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-soft text-primary">
              <Upload className="h-6 w-6" />
            </div>
            <h3 className="mt-4 font-medium">Drop your files here</h3>
            <p className="mt-1 text-sm text-muted-foreground">CSV or PDF, up to 20 MB each</p>
            <Button type="button" className="mt-4">Choose files</Button>
            <input
              ref={inputRef}
              type="file"
              multiple
              accept=".csv,.pdf"
              className="hidden"
              onChange={(e) => onFiles(e.target.files)}
            />
          </div>
        </CardContent>
      </Card>

      {files.length > 0 && (
        <Card className="shadow-[var(--shadow-soft)]">
          <CardHeader>
            <CardTitle>Uploaded files</CardTitle>
            <CardDescription>{files.length} file(s) ready for analysis</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {files.map((f, i) => (
              <div key={i} className="flex items-center justify-between rounded-xl border p-3">
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-secondary">
                    <FileText className="h-4 w-4 text-muted-foreground" />
                  </div>
                  <div>
                    <div className="text-sm font-medium">{f.name}</div>
                    <div className="text-xs text-muted-foreground">{(f.size / 1024).toFixed(1)} KB</div>
                  </div>
                </div>
                <Badge variant="secondary" className="gap-1">
                  <CheckCircle2 className="h-3 w-3" /> Ready
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

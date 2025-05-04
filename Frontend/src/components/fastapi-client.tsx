
"use client";

import * as React from "react";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Send, Link as LinkIcon, Trash2, AlertCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const API_BASE_URL = "http://localhost:8000"; // Default FastAPI backend URL

export default function FastAPIClient() {
  const [url, setUrl] = useState<string>("https://quotes.toscrape.com/");
  const [maxDepth, setMaxDepth] = useState<number>(1);
  const [question, setQuestion] = useState<string>("“Imperfection is beauty...”");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loadingIngest, setLoadingIngest] = useState<boolean>(false);
  const [loadingAsk, setLoadingAsk] = useState<boolean>(false);
  const [loadingReset, setLoadingReset] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const { toast } = useToast();

  const handleIngest = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingIngest(true);
    setError(null);
    setAnswer(null); // Clear previous answer

    try {
      const response = await fetch(
        `${API_BASE_URL}/ingest-url/?url=${encodeURIComponent(url)}&max_depth=${maxDepth}`,
        {
          method: "POST",
          headers: {
            "accept": "application/json",
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown ingestion error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      toast({
        title: "Success",
        description: `URL ingested successfully. ${result.message || ''}`,
        variant: "default",
      });

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "An unexpected error occurred during ingestion.";
      setError(`Ingestion failed: ${errorMessage}`);
      toast({
        title: "Error",
        description: `Ingestion failed: ${errorMessage}`,
        variant: "destructive",
      });
    } finally {
      setLoadingIngest(false);
    }
  };

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingAsk(true);
    setError(null);
    setAnswer(null);

    try {
      console.log("Sending question to API:", question);
    
      const response = await fetch(
        `${API_BASE_URL}/ask-question/?question=${encodeURIComponent(question)}`,
        {
          method: "POST",
          headers: {
            "accept": "application/json",
          },
        }
      );
    
      console.log("Response status:", response.status);
    
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown question asking error' }));
        console.error("Error response data:", errorData);
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
    
      const result = await response.json();
      console.log("API result:", result);
    
      setAnswer(result.answer || "No answer found."); // Assuming the API returns { "answer": "..." }
    
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "An unexpected error occurred asking the question.";
      console.error("Fetch error:", err);
      setError(`Asking question failed: ${errorMessage}`);
      toast({
        title: "Error",
        description: `Asking question failed: ${errorMessage}`,
        variant: "destructive",
      });
    } finally {
      setLoadingAsk(false);
    }
    

   const handleReset = async () => {
    setLoadingReset(true);
    setError(null);
    setAnswer(null); // Clear answer on reset

    try {
      const response = await fetch(`${API_BASE_URL}/reset-embeddings/`, {
        method: "DELETE",
        headers: {
          "accept": "application/json",
        },
      });

       if (!response.ok) {
         const errorData = await response.json().catch(() => ({ detail: 'Unknown reset error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      await response.json(); // Consume the response body
      toast({
        title: "Success",
        description: "Embeddings reset successfully.",
        variant: "default",
      });

    } catch (err) {
       const errorMessage = err instanceof Error ? err.message : "An unexpected error occurred during reset.";
       setError(`Reset failed: ${errorMessage}`);
       toast({
        title: "Error",
        description: `Reset failed: ${errorMessage}`,
        variant: "destructive",
      });
    } finally {
      setLoadingReset(false);
    }
  };


  return (
    // Adjusted background transparency
    <div className="w-full max-w-2xl space-y-8 p-4 bg-card/90 backdrop-blur-sm rounded-xl shadow-lg">
       {/* Apply cursive font and increase size, change color to white */}
       <h1 className="text-7xl font-bold text-center text-white font-cursive pt-4">Scrapper-Bot</h1>

       {error && (
         <Alert variant="destructive">
           <AlertCircle className="h-4 w-4" />
           <AlertTitle>Error</AlertTitle>
           <AlertDescription>{error}</AlertDescription>
         </Alert>
       )}

       {/* Ingest URL Card */}
       <Card className="shadow-md transition-shadow hover:shadow-lg">
         <CardHeader>
           <CardTitle className="flex items-center gap-2">
             <LinkIcon className="h-5 w-5 text-accent" />
             Ingest URL
           </CardTitle>
           <CardDescription>Enter a URL and max depth to fetch and process content.</CardDescription>
         </CardHeader>
         <form onSubmit={handleIngest}>
           <CardContent className="space-y-4">
             <Input
               type="url"
               placeholder="https://example.com"
               value={url}
               onChange={(e) => setUrl(e.target.value)}
               required
               className="focus:ring-accent"
             />
             <Input
                type="number"
                placeholder="Max Depth (e.g., 1)"
                value={maxDepth}
                onChange={(e) => setMaxDepth(parseInt(e.target.value, 10) || 0)}
                min="0"
                required
                 className="focus:ring-accent"
              />
           </CardContent>
           <CardFooter>
             <Button type="submit" disabled={loadingIngest || loadingAsk || loadingReset} className="w-full bg-primary hover:bg-primary/90 text-primary-foreground">
               {loadingIngest ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <LinkIcon className="mr-2 h-4 w-4" />}
               Ingest URL
             </Button>
           </CardFooter>
         </form>
       </Card>

       {/* Ask Question Card */}
       <Card className="shadow-md transition-shadow hover:shadow-lg">
         <CardHeader>
           <CardTitle className="flex items-center gap-2">
             <Send className="h-5 w-5 text-accent" />
              Ask a Question
           </CardTitle>
           <CardDescription>Ask a question based on the ingested content.</CardDescription>
         </CardHeader>
          <form onSubmit={handleAsk}>
           <CardContent className="space-y-4">
             <Textarea
               placeholder="Your question..."
               value={question}
               onChange={(e) => setQuestion(e.target.value)}
               required
               className="focus:ring-accent"
             />
              {answer && (
                <div className="mt-4 rounded-md border bg-secondary p-4">
                  <p className="text-sm font-medium text-secondary-foreground">Answer:</p>
                  <p className="text-sm text-secondary-foreground/90">{answer}</p>
                </div>
             )}
           </CardContent>
           <CardFooter>
             <Button type="submit" disabled={loadingAsk || loadingIngest || loadingReset} className="w-full bg-primary hover:bg-primary/90 text-primary-foreground">
               {loadingAsk ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Send className="mr-2 h-4 w-4" />}
               Ask Question
             </Button>
           </CardFooter>
         </form>
       </Card>

        {/* Reset Embeddings Button */}
        <div className="flex justify-center">
            <Button
                variant="destructive"
                onClick={handleReset}
                disabled={loadingReset || loadingIngest || loadingAsk}
                className="w-full md:w-auto transition-colors duration-200 ease-in-out"
            >
                {loadingReset ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Trash2 className="mr-2 h-4 w-4" />}
                Reset Embeddings
            </Button>
        </div>

        {/* Instructions Card - adjusted transparency */}
        <Card className="mt-8 bg-muted/85 shadow-inner">
         <CardHeader>
           <CardTitle className="text-lg">How to Run</CardTitle>
         </CardHeader>
         <CardContent className="space-y-2 text-sm text-muted-foreground">
           <p>1. Ensure your FastAPI backend is running (usually on <code className="font-mono bg-secondary/90 px-1 rounded">http://localhost:8000</code>).</p>
           <p>2. Start this Next.js frontend application using <code className="font-mono bg-secondary/90 px-1 rounded">npm run dev</code>.</p>
           <p>3. Use the form above to interact with your FastAPI backend.</p>
            <p>4. Check your browser's developer console (F12) and the terminal running FastAPI for logs and potential errors.</p>
            <p>5. Make sure CORS is configured correctly in your FastAPI backend to allow requests from this frontend (usually <code className="font-mono bg-secondary/90 px-1 rounded">http://localhost:9002</code> or your Next.js dev server port).</p>
         </CardContent>
        </Card>
    </div>
  );
}


import FastAPIClient from '@/components/fastapi-client';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-8">
       {/* Add a container with padding if needed, especially with a background image */}
       <div className="container mx-auto flex items-center justify-center">
         <FastAPIClient />
       </div>
    </main>
  );
}

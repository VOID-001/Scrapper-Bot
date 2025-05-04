import type {Metadata} from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import { Dancing_Script } from 'next/font/google'; // Import cursive font
import './globals.css';
import { Toaster } from "@/components/ui/toaster"

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

// Initialize cursive font
const dancingScript = Dancing_Script({
  variable: '--font-dancing-script',
  subsets: ['latin'],
  weight: ['400', '700'], // Specify weights if needed
});

export const metadata: Metadata = {
  title: 'Scrapper-Bot', // Updated title
  description: 'Simple frontend for FastAPI backend',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // Add dark class here
    <html lang="en" className="dark">
      {/* Add cursive font variable */}
      <body className={`${geistSans.variable} ${geistMono.variable} ${dancingScript.variable} antialiased`} data-ai-hint="minimalist pattern geometric abstract">
        {children}
        <Toaster />
      </body>
    </html>
  );
}

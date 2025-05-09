'use client'

import Movie from "@/components/ui/movie";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-start w-full flex-1">
      <ScrollArea className="w-full h-full max-w-5xl flex flex-col flex-grow overflow-y-auto">
        <h2 className="text-2xl font-medium my-2">Recommendations:</h2>
        <Movie title="The Chronicles of Narnia: The Lion, the Witch and the Wardrobe"></Movie>
        <h2 className="text-2xl font-medium my-2">Movies:</h2>
      </ScrollArea>
    </main>
  );
}

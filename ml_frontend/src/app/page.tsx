'use client'

import { Button } from "@/components/ui/button";
import Movie from "@/components/ui/movie";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-start w-full flex-1">
      <ScrollArea className="w-full h-full max-w-5xl flex flex-col flex-grow overflow-y-auto">
        <h2 className="text-2xl font-medium my-2">Recommendations:</h2>
        <div className="py-2 grid grid-cols-5 w-full items-center justify-center">
          <Movie title="The Chronicles of Narnia: The Lion, the Witch and the Wardrobe"/>
          <Movie title="Avatar"/>
          <Movie title="Pirates of the Caribbean: At World's End"/>
          <Movie title="Spectre"/>
          <Movie title="The Dark Knight Rises"/>
        </div>
        <h2 className="text-2xl font-medium my-2">Movies:</h2>
        <div className="py-2 grid grid-cols-5 w-full items-center justify-center">
          <Movie title="John Carter"/>
          <Movie title="Spider-Man 3"/>
          <Movie title="Tangled"/>
          <Movie title="Avengers: Age of Ultron"/>
          <Movie title="The Avengers"/>
          <Movie title="The Chronicles of Narnia: The Lion, the Witch and the Wardrobe"/>
          <Movie title="Avatar"/>
          <Movie title="Pirates of the Caribbean: At World's End"/>
          <Movie title="Spectre"/>
          <Movie title="The Dark Knight Rises"/>
        </div>
      </ScrollArea>
    </main>
  );
}

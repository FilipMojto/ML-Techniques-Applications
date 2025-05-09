'use client'

import { Button } from "@/components/ui/button";
import Movie from "@/components/ui/movie";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-start w-full flex-1 overflow-hidden">
      <ScrollArea className="w-full max-w-full h-full max-h-full">
        <div className="flex flex-col justify-start items-center w-full">
          <div className="max-w-11/12 w-5xl flex flex-col">
            <h2 className="text-2xl font-medium my-4">Recommendations:</h2>
            <div className="py-2 grid grid-cols-5 min-w-full w-fit items-center justify-center shrink-0">
              <Movie title="The Chronicles of Narnia: The Lion, the Witch and the Wardrobe"/>
              <Movie title="Avatar"/>
              <Movie title="Pirates of the Caribbean: At World's End"/>
              <Movie title="Spectre"/>
              <Movie title="The Dark Knight Rises"/>
            </div>
            <h2 className="text-2xl font-medium my-4">Movies:</h2>
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
            <div className="py-2 flex flex-row w-full justify-center mb-8">
              <Button>Load More</Button>
            </div>
          </div>
        </div>
      </ScrollArea>
    </main>
  );
}

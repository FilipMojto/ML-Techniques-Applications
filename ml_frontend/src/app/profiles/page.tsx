'use client'

import Movie from "@/components/ui/movie";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";

export default function Profile() {
  return (
    <main className="flex flex-col items-center justify-start w-full flex-1 overflow-hidden">
      <ScrollArea className="w-full max-w-full h-full max-h-full">
        <div className="flex flex-col justify-start items-center w-full">
          <div className="max-w-11/12 w-5xl flex flex-col">
            <h2 className="text-2xl font-medium my-4">User Info:</h2>
            <div className="flex flex-row justify-between items-center px-4 pb-8">
              <div className="flex flex-row items-center">
                <Avatar className="h-24 w-24">
                  <AvatarFallback>
                    <span className="font-semibold text-4xl">JD</span>
                  </AvatarFallback>
                </Avatar>
                <p className="text-2xl font-medium ml-4">
                  John Doe
                </p>
              </div>
              <Button variant="destructive">
                Log Out
              </Button>
            </div>
            <h2 className="text-2xl font-medium my-4">Liked Movies:</h2>
            <div className="py-2 grid grid-cols-5 w-full items-center justify-center">
              <Movie title="John Carter" />
              <Movie title="Spider-Man 3" />
              <Movie title="Tangled" />
              <Movie title="Avengers: Age of Ultron" />
              <Movie title="The Avengers" />
            </div>
          </div>
        </div>
      </ScrollArea>
    </main>
  );
}
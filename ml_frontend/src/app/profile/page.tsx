'use client'

import MovieCard from "@/components/ui/movie-card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { toast } from 'sonner';
import { useRouter, useParams } from 'next/navigation';
import { deleteCookie, getCookie } from 'cookies-next/client';
import { useEffect, useState } from 'react';
import { User, Movie, useUser } from '@/components/user-provider'


export default function Profile() {
  const router = useRouter();
  const { user, setUser } = useUser();

  const fallbackChars = (name: string) => {
    let words = name.split(" ");
    let fallback = "";

    words.forEach((word) => {
      fallback = fallback + word.charAt(0);
    })

    return fallback.toUpperCase();
  }

  const handleLogout = () => {
    toast.success('Logout successful');
    deleteCookie("user");
    setTimeout(() => {
      router.push('/login');
    }, 500);
  }

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
                    <span className="font-semibold text-4xl">{fallbackChars(user ? user.username : "")}</span>
                  </AvatarFallback>
                </Avatar>
                <p className="text-2xl font-medium ml-4">
                  {user?.username}
                </p>
              </div>
              <Button onClick={handleLogout} variant="destructive">
                Logout
              </Button>
            </div>
            <h2 className="text-2xl font-medium my-4">Liked Movies:</h2>
            <div className="py-2 grid grid-cols-5 w-full items-center justify-center">
              {user && user!.liked_movies.map((movie) => (
                <MovieCard key={movie.movie_id} movie={movie}/>
              ))}
            </div>
          </div>
        </div>
      </ScrollArea>
    </main>
  );
}
'use client'

import MovieCard from "@/components/ui/movie-card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { useRouter, useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { User } from '@/components/user-provider'


export default function Profile() {
  const router = useRouter();
  const params = useParams();
  const username = params.username as string;
  const [user, setUser] = useState<User>();

  const fallbackChars = (name: string) => {
    const words = name.split(" ");
    let fallback = "";

    words.forEach((word) => {
      fallback = fallback + word.charAt(0);
    })

    return fallback.toUpperCase();
  }

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch('/api/user', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username }),
        });
        if (!res.ok) {
          router.push("/users");
          return;
        };
        const data: User = await res.json();
        setUser(data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchUser();
  }, []);

  return (
    <main className="flex flex-col items-center justify-start w-full flex-1 overflow-hidden">
      <div className="flex flex-col justify-start items-center w-full overflow-y-auto">
        <div className="max-w-11/12 w-5xl flex flex-col">
          <h2 className="text-2xl font-medium my-4">User Info:</h2>
          <div className="flex flex-row justify-between items-center px-4 pb-8">
            <div className="flex flex-row items-center">
              <Avatar className="h-24 w-24">
                <AvatarFallback>
                  <span className="font-semibold text-4xl">{fallbackChars(username)}</span>
                </AvatarFallback>
              </Avatar>
              <p className="text-2xl font-medium ml-4">
                {username}
              </p>
            </div>
          </div>
          <h2 className="text-2xl font-medium my-4">Liked Movies:</h2>
          <div className="py-2 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 w-full items-center justify-center">
            {user && user!.liked_movies.map((movie) => (
              <MovieCard key={movie.movie_id} movie={movie} />
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
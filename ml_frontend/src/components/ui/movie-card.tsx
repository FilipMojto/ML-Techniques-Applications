"use client";

import { Button } from "./button";
import { Heart } from "lucide-react";
import { toast } from "sonner";
import { useUser, Movie } from "../user-provider";

export type MovieProps = {
  movie: Movie;
  disable_like?: boolean;
}

export default function MovieCard({ movie, disable_like = false }: MovieProps) {
  const { user, like, dislike } = useUser();

  const liked = user?.liked_movies.some(m => m.movie_id === movie.movie_id) ?? false;

  const coverLetter = (title: string) => {
    return title.charAt(0).toUpperCase();
  }

  const randomColor = (title: string): string => {
    // Simple hash function from string to number
    let hash = 0;
    for (let i = 0; i < title.length; i++) {
      hash = title.charCodeAt(i) + ((hash << 5) - hash);
    }

    hash *= 2.56789

    // Use the hash to get a hue value between 0 and 359
    const hue = Math.abs(hash % 360);
    const saturation = 50;
    const lightness = 75;

    return `hsl(${hue},${saturation}%,${lightness}%)`;
  };

  const handleLike = () => {
    like(movie);
    toast.success('Movie added to liked movies')
  }

  const handleDisike = () => {
    dislike(movie);
    toast.success('Movie removed from liked movies')
  }

  return (
    <div className="flex flex-row justify-center col-span-1">
      <div className="flex flex-col h-80 w-44 justify-start items-center">
        <div className={`flex flex-row h-60 w-44 items-center justify-center rounded-sm relative
        hover:scale-105 transition-transform duration-200`}
          style={{ backgroundColor: randomColor(movie.title) }}>
          {!disable_like && !liked &&
            <Button variant="ghost" size="icon" className="w-8 h-8 absolute top-2 right-2 hover:bg-accent/50"
              onClick={handleLike}>
              <Heart strokeWidth={3} className="text-destructive" />
            </Button>}
          {!disable_like && liked &&
            <Button variant="ghost" size="icon" className="w-8 h-8 absolute top-2 right-2 hover:bg-accent/50"
              onClick={handleDisike}>
              <Heart strokeWidth={3} className="fill-destructive text-destructive" />
            </Button>}
          <span className="text-8xl font-medium text-white">{coverLetter(movie.title)}</span>
        </div>
        <span className="w-full line-clamp-3 text-sm font-medium text-center my-2">
          {movie.title.trim()}
        </span>
      </div>
    </div>
  )
}
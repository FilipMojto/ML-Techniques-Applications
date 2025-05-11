'use client'

import { Button } from "@/components/ui/button";
import MovieCard from "@/components/ui/movie-card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { LoaderCircle, RefreshCw } from "lucide-react";
import { useState, useEffect } from "react";
import { useMovies } from '@/components/movie-provider';
import { getCookie } from 'cookies-next/client';
import { Movie } from "@/components/movie-provider";

export type Recommendation = { title: string; similarity: number };

export default function Home() {

  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const { movies, fetchMovies } = useMovies();
  const username = getCookie("user");

  const fetchRecommendations = async () => {
    try {
      const res = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });
      if (!res.ok) {
        return;
      };
      const data: Recommendation[] = await res.json();
      setRecommendations(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (movies.length == 0) {
      fetchMovies(0, 20);
    }
    fetchRecommendations();
  }, []);

  const loadMore = async () => {
    setLoading(true);
    await fetchMovies(movies.length, 20);
    setLoading(false);
  }

  return (
    <main className="flex flex-col items-center justify-start w-full flex-1 overflow-hidden">
      <ScrollArea className="w-full max-w-full h-full max-h-full">
        <div className="flex flex-col justify-start items-center w-full">
          <div className="max-w-11/12 w-5xl flex flex-col">
            {recommendations.length > 0 &&
              <>
                <h2 className="text-2xl font-medium my-4">Recommendations:</h2>
                <div className="py-2 grid grid-cols-5 min-w-full w-fit items-center justify-center shrink-0">
                  {recommendations.map((recommendation, index) => (
                    <MovieCard key={index} movie={{ title: recommendation.title, movie_id: 0 }} disable_like={true} />
                  ))}
                </div>
              </>}
            <h2 className="text-2xl font-medium my-4">Movies:</h2>
            <div className="py-2 grid grid-cols-5 w-full items-center justify-center">
              {movies.map((movie) => (
                <MovieCard key={movie.movie_id} movie={movie} />
              ))}
            </div>
            <div className="py-2 flex flex-row w-full justify-center mb-8">
              <Button onClick={loadMore} disabled={loading}>
                {loading && <LoaderCircle className="animate-spin" />}
                {!loading && <RefreshCw />}
                Load More
              </Button>
            </div>
          </div>
        </div>
      </ScrollArea>
    </main>
  );
}

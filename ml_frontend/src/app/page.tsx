'use client'

import { Button } from "@/components/ui/button";
import MovieCard from "@/components/ui/movie-card";
import { LoaderCircle, RefreshCw } from "lucide-react";
import { useState, useEffect } from "react";
import { useMovies } from '@/components/movie-provider';
import { getCookie } from 'cookies-next/client';
import { useUser } from "@/components/user-provider";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"


export type Recommendation = { title: string; similarity: number };

export default function Home() {

  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const { movies, fetchMovies } = useMovies();
  const { user } = useUser();
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
  }, [fetchMovies, movies.length]);

  useEffect(() => {
    fetchRecommendations();
  }, [user?.liked_movies]);

  const loadMore = async () => {
    setLoading(true);
    await fetchMovies(movies.length, 20);
    setLoading(false);
  }

  return (
    <main className="flex flex-col items-center justify-start w-full max-w-full flex-1 overflow-hidden">
      <div className="flex flex-col justify-start items-center w-full max-w-full overflow-y-auto">
        <div className="max-w-10/12 xl:max-w-11/12 w-5xl flex min-w-0 flex-col flex-shrink">
          {recommendations.length > 0 &&
            <>
              <h2 className="text-2xl font-medium my-4">Recommendations:</h2>
              <Carousel
                className="mx-2"
                opts={{
                  align: "start",
                }}>
                <CarouselContent className="py-2">
                  {recommendations.map((recommendation, index) => (
                    <CarouselItem key={index} className="basis-1/2 md:basis-1/3 lg:basis-1/4 xl:basis-1/5">
                      <MovieCard movie={{ title: recommendation.title, movie_id: 0 }} disable_like={true} />
                    </CarouselItem>
                  ))}
                </CarouselContent>
                <CarouselPrevious />
                <CarouselNext />
              </Carousel>
            </>}
          <h2 className="text-2xl font-medium my-4">Movies:</h2>
          <div className="py-2 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 w-full items-center justify-center">
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
    </main>
  );
}

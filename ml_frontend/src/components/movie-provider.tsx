'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

export type Movie = { movie_id: number; title: string };

type MovieContextType = {
  movies: Movie[];
  setMovies: (movies: Movie[]) => void;
  fetchMovies: (skip: number, limit: number) => Promise<void>;
};

const MovieContext = createContext<MovieContextType | undefined>(undefined);

export const useMovies = () => {
  const context = useContext(MovieContext);
  if (!context) throw new Error('useMovies must be used within a MoviesProvider');
  return context;
};

export const MovieProvider = ({ children }: { children: ReactNode }) => {
  const [movies, setMovies] = useState<Movie[]>([]);

  const fetchMovies = async (skip: number, limit: number) => {
    try {
      const res = await fetch('/api/movies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ skip, limit }),
      });
      if (!res.ok) throw new Error('Failed to fetch movies');
      const data: Movie[] = await res.json();
      setMovies(prev => [...prev, ...data]);
    } catch (err) {
      console.error('Error fetching movies:', err);
    }
  };

  return (
    <MovieContext.Provider value={{ movies, setMovies, fetchMovies }}>
      {children}
    </MovieContext.Provider>
  );
};
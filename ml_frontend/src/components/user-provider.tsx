'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export type Movie = {
  movie_id: number;
  title: string;
};

export type User = {
  username: string;
  user_id: number;
  liked_movies: Movie[];
};

type UserContextType = {
  user: User | null;
  setUser: (user: User) => void;
  like: (movie: Movie) => Promise<void>;
  dislike: (movie: Movie) => Promise<void>;
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error('useUser must be used within a UserProvider');
  return context;
};

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, _setUser] = useState<User | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        _setUser(JSON.parse(storedUser));
      } catch (err) {
        console.error('Failed to parse stored user:', err);
      }
    }
  }, []);

  const setUser = (user: User) => {
    _setUser(user);
    localStorage.setItem('user', JSON.stringify(user));
  };

  const like = async (movie: Movie) => {
    if (!user) return;
    try {
      const res = await fetch(`/api/like`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          movie_id: movie.movie_id,
          username: user.username,
        }),
      });
      if (!res.ok) throw new Error('Failed to like movie');

      const updatedUser = {
        ...user,
        liked_movies: [...user.liked_movies, movie],
      };
      setUser(updatedUser);
    } catch (err) {
      console.error(err);
    }
  };

  const dislike = async (movie: Movie) => {
    if (!user) return;
    try {
      const res = await fetch(`/api/dislike`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          movie_id: movie.movie_id,
          username: user.username,
        }),
      });
      if (!res.ok) throw new Error('Failed to dislike movie');

      const updatedUser = {
        ...user,
        liked_movies: user.liked_movies.filter(m => m.movie_id !== movie.movie_id),
      };
      setUser(updatedUser);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <UserContext.Provider value={{ user, setUser, like, dislike }}>
      {children}
    </UserContext.Provider>
  );
};
"use client";

import { Button } from "./button";
import { Card, CardContent, CardFooter, CardTitle } from "./card";
import { Heart } from "lucide-react";

export type MovieProps = {
  title: string;
}

export default function Movie({title}: MovieProps) {

  const coverLetter = (title: string) => {
    return title.charAt(0).toUpperCase();
  }

  return (
    <div className="flex flex-col h-70 w-44 justify-between items-center">
      <div className="flex flex-row h-60 w-44 items-center justify-center rounded-sm bg-blue-500 relative">
        <Button variant="ghost" size="icon" className="w-8 h-8 absolute top-2 right-2 hover:bg-transparent hover:outline-2 text-white hover:text-white">
          <Heart/>
        </Button>
        <span className="text-white text-8xl font-medium">{coverLetter(title)}</span>
      </div>
      <span className="w-full line-clamp-1 text-sm font-medium text-center my-2">
        {title.trim()}
      </span>
    </div>
  )
}
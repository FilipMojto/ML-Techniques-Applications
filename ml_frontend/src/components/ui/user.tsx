'use client'

import { Avatar, AvatarFallback } from "./avatar";
import { Button } from "./button";
import { Card } from "./card";

export type UserProps = {
  name: string;
}

export default function User({ name }: UserProps) {

  const fallbackChars = (name: string) => {
    let words = name.split(" ");
    let fallback = "";

    words.forEach((word) => {
      fallback = fallback + word.charAt(0);
    })

    return fallback.toUpperCase();
  }

  return (
    <Card className="flex flex-row w-full py-2 px-4 justify-between items-center hover:scale-[101.5%] transition-transform duration-200">
      <div className="flex flex-row items-center">
        <Avatar className="h-14 w-14">
          <AvatarFallback>
            <span className="font-medium text-xl">{fallbackChars(name)}</span>
          </AvatarFallback>
        </Avatar>
        <p className="text-lg font-medium ml-4">
          {name}
        </p>
      </div>
      <Button>
        Open Profile
      </Button>
    </Card>
  );
}
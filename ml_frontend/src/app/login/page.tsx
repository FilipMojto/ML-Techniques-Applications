'use client'

import Movie from "@/components/ui/movie";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";

export default function LogIn() {
  return (
    <main className="flex flex-col items-center justify-center w-full flex-1 overflow-hidden">
      <Card className="w-80 h-96 flex flex-col justify-between">
        <CardHeader>
          <CardTitle className="text-lg">Log In</CardTitle>
        </CardHeader>
        <CardContent>
          <form>
            <Label className="py-2">Username</Label>
            <Input placeholder="Your Username"></Input>
          </form>
        </CardContent>
        <div className="flex flex-col px-6 py-3">
          <Button className="w-full">Log In</Button>
          <div className="flex flex-row items-center py-6 justify-center">
            <Separator className="flex flex-1/4" />
            <span className="flex flex-1/2 text-sm justify-center">Or Register</span>
            <Separator className="flex flex-1/4" />
          </div>
          <Button className="w-full">Register</Button>
        </div>
      </Card>
    </main>
  );
}
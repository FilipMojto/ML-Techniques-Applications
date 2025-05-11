'use client'

import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { useRouter } from 'next/navigation';
import { useRef } from 'react';
import { toast } from 'sonner';
import { setCookie } from 'cookies-next/client';
import { User, useUser } from '@/components/user-provider'

export default function LogIn() {
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();
  const { setUser } = useUser();

  const handleLogin = async () => {
    const username = inputRef.current?.value.trim();
    inputRef.current!.value = "";
    if (!username) return toast.warning('Please enter a username');

    const res = await fetch('/api/user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username }),
    });

    if (res.ok) {
      const data: User = await res.json();
      setUser(data);
      toast.success('Login successful');
      await setCookie("user", username);
      router.push('/');
      setTimeout(()=>{
        router.refresh();
        router.push('/');
      }, 500);

    } else if (res.status === 404) {
      toast.error('Incorrect username');
    } else {
      toast.error('Something went wrong. Try again later');
    }
  };

  const handleRegister = async () => {
    const username = inputRef.current?.value.trim();
    inputRef.current!.value = "";
    if (!username) return toast.warning('Please enter a username');

    const res = await fetch('/api/add-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username }),
    });

    if (res.ok) {
      const data: User = await res.json();
      setUser(data);
      toast.success('Register successful');
      await setCookie("user", username);
      router.push('/');
      setTimeout(()=>{
        router.refresh();
        router.push('/');
      }, 500);

    } else if (res.status === 409) {
      toast.error('Username already in use');
    } else {
      toast.error('Something went wrong. Try again later');
    }
  };

  return (
    <main className="flex flex-col items-center justify-center w-full flex-1 overflow-hidden">
      <Card className="w-80 h-96 flex flex-col justify-between">
        <CardHeader>
          <CardTitle className="text-lg">Log In</CardTitle>
        </CardHeader>
        <CardContent>
          <Label className="py-2">Username</Label>
          <Input ref={inputRef} placeholder="Your Username" />
        </CardContent>
        <div className="flex flex-col px-6 py-3">
          <Button onClick={handleLogin} className="w-full">Log In</Button>
          <div className="flex flex-row items-center py-6 justify-center">
            <Separator className="flex flex-1/3" />
            <span className="flex flex-1/3 text-sm justify-center">Or</span>
            <Separator className="flex flex-1/3" />
          </div>
          <Button onClick={handleRegister} className="w-full">Register</Button>
        </div>
      </Card>
    </main>
  );
}
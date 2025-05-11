import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  try {
    const res = await fetch(`${baseUrl}/movies/dislike`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      return new NextResponse('Failed to dislike movie', { status: res.status });
    }

    return new NextResponse('Movie disliked successfully', { status: 200 });
  } catch (error) {
    console.error(error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}

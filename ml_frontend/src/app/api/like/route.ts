import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const baseUrl = process.env.BACKEND_URL ??  "http://localhost:5000";

  try {
    const res = await fetch(`${baseUrl}/movies/like`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      return new NextResponse('Failed to like movie', { status: res.status });
    }

    return new NextResponse('Movie liked successfully', { status: 200 });
  } catch (error) {
    console.error(error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
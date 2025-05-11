import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { skip = 0, limit = 20 } = await req.json();
    const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    const res = await fetch(`${baseUrl}/movies?skip=${skip}&limit=${limit}`);

    if (!res.ok) {
      return new NextResponse('Failed to fetch movies', { status: res.status });
    }

    const movies = await res.json();

    return new NextResponse(JSON.stringify(movies), {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Movie fetch error:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
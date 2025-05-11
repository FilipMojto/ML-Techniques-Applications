import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const baseUrl = process.env.BACKEND_URL ??  "http://localhost:5000";

    const res = await fetch(`${baseUrl}/user/all`);

    if (!res.ok) {
      return new NextResponse('Failed to fetch users', { status: res.status });
    }

    const movies = await res.json();

    return new NextResponse(JSON.stringify(movies), {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('User fetch error:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { username, no_of_recommendations = 5 } = await req.json();
    const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    const res = await fetch(`${baseUrl}/recommend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, no_of_recommendations }),
    });

    if (!res.ok) {
      return new NextResponse('Failed to fetch recommendation', { status: res.status });
    }

    const data = await res.json();

    return new NextResponse(JSON.stringify(data.recommendations), {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Recommendation fetch error:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
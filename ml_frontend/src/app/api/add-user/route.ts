import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const body = await req.json();

  const baseUrl = process.env.BACKEND_URL ??  "http://localhost:5000";

  try {
    const userRes = await fetch(`${baseUrl}/user`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (userRes.status === 409) {
      return new NextResponse('User already exists', { status: 409 });
    }

    if (!userRes.ok) {
      return new NextResponse('Internal Server Error', { status: 500 });
    }

    const user = await userRes.json();

    return new NextResponse(JSON.stringify(user), {
      headers: {
        'Content-Type': 'application/json'
      },
    });
  } catch {
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
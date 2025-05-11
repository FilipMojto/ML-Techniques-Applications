import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  let body = await req.json();

  const username = body.username;
  const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  try {
    const userRes = await fetch(`${baseUrl}/user/${username}`);

    if (userRes.status === 404) {
      return new NextResponse('User not found', { status: 404 });
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
  } catch (err) {
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
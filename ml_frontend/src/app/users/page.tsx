'use client'

import UserCard from "@/components/ui/user";
import { useEffect, useState } from 'react';
import { User } from '@/components/user-provider'
import { useUser } from "@/components/user-provider";

export default function Users() {
  const [users, setUsers] = useState<User[]>([]);
  const { user } = useUser();

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch('/api/users');
        if (!res.ok) throw new Error('Failed to fetch users');
        const data: User[] = await res.json();
        setUsers(data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchUsers();
  }, []);

  return (
    <main className="flex flex-col items-center justify-start w-full flex-1 overflow-hidden">
        <div className="flex flex-col justify-start items-center w-full overflow-y-auto pb-4">
          <div className="max-w-10/12 xl:max-w-11/12 w-5xl flex min-w-0 flex-col flex-shrink">
            <h2 className="text-2xl font-medium my-4">Users:</h2>
            <div className="grid grid-cols-1 gap-4 px-4">
              {users
              .filter(u => u.user_id !== user?.user_id)
              .map((user) => (
                <UserCard key={user.user_id} name={user.username} />
              ))}
            </div>
          </div>
        </div>
    </main>
  );
}

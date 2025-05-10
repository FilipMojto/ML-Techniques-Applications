import { ScrollArea } from "@/components/ui/scroll-area";
import User from "@/components/ui/user";

export default function Users() {
  return (
    <main className="flex flex-col items-center justify-start w-full flex-1 overflow-hidden">
      <ScrollArea className="w-full max-w-full h-full max-h-full">
        <div className="flex flex-col justify-start items-center w-full">
          <div className="max-w-11/12 w-5xl flex flex-col">
            <h2 className="text-2xl font-medium my-4">Users:</h2>
            <div className="grid grid-cols-1 gap-4 px-4">
              <User name="John Doe" />
              <User name="Johnyboy" />
              <User name="John Doe" />
              <User name="John Doe" />
              <User name="John Doe" />
              <User name="John Doe" />
              <User name="John Doe" />
              <User name="John Doe" />
              <User name="John Doe" />
              <User name="John Doe" />
            </div>
          </div>
        </div>
      </ScrollArea>
    </main>
  );
}

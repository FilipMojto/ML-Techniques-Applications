import { ScrollArea } from "@/components/ui/scroll-area";

export default function Users() {
  return (
    <main className="flex flex-col items-center justify-start w-full flex-1">
      <ScrollArea className="w-full h-full max-w-5xl flex flex-col flex-grow overflow-y-auto">
        <h2 className="text-2xl font-medium my-2">Users:</h2>
        
      </ScrollArea>
    </main>
  );
}

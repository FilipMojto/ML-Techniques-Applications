"use client";

import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
  navigationMenuTriggerStyle,
} from "./navigation-menu";
import { useRouter } from "next/navigation";
import { Separator } from "./separator";
import ThemeToggle from "./theme-toggle";

export default function Header() {
  const router = useRouter()
  return (
    <div className="flex flex-col items-center justify-center">
      <div className="flex flex-row justify-between items-center w-full">
        <div className="w-9 ml-2" />
        <NavigationMenu className="py-2">
          <NavigationMenuList>
            <NavigationMenuItem onClick={()=>{router.push("/")}}>
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Movies
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem onClick={()=>{router.push("/users")}}>
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Users
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem onClick={()=>{router.push("/profile")}}>
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Profile
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
        <ThemeToggle />
      </div>
      <Separator />
    </div>
  );
};

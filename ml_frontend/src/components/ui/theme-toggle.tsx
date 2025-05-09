"use client"

import { Moon, Sun, Laptop } from "lucide-react";
import { useState, useEffect } from "react";
import { Button } from "./button";

export default function ThemeToggle() {

  const [theme, setTheme] = useState('system');

  useEffect(() => {
    // Retrieve the theme from localStorage only if it is available (browser environment)
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setTheme(savedTheme);
    }
  }, []);

  // Update <html> class and save to localStorage whenever theme changes
  useEffect(() => {
    document.documentElement.classList.toggle(
      'dark',
      theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
    )

    // Save the user's theme choice to localStorage
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Function to toggle the theme
  const cycleTheme = () => {
    if (theme === "system") {
      setTheme("light");
    } else if (theme === "light") {
      setTheme("dark");
    } else {
      setTheme("system");
    }
  };

  const renderIcon = () => {
    if (theme === "dark") return <Moon className="h-4 w-4" />;
    if (theme === "light") return <Sun className="h-4 w-4" />;
    return <Laptop className="h-4 w-4" />;
  };

  return (
    <Button size="icon" variant="outline" className="mr-2" onClick={cycleTheme}>
      {renderIcon()}
    </Button>
  );
}
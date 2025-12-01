import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SidebarState {
  collapsed: boolean;
  setCollapsed: (value: boolean) => void;
  toggle: () => void;
}

export const useSidebarStore = create<SidebarState>()(
  persist(
    (set, get) => ({
      collapsed: false,
      setCollapsed: (value: boolean) => set({ collapsed: value }),
      toggle: () => set({ collapsed: !get().collapsed }),
    }),
    {
      name: "sidebar-storage",
    }
  )
);

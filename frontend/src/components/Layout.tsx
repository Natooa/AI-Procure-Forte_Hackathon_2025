import {
  SidebarProvider,
  SidebarTrigger,
  SidebarInset,
} from "@/components/ui/sidebar";
import { AppSidebar } from "./AppSidebar";
import { ModeToggle } from "./ModeToggle";
import { useSidebarStore } from "@/store/useSidebarStore.ts";
import { Toaster } from "sonner";
import { UploadTenderDialog } from "./UploadTenderDialog";

export default function Layout({ children }: { children: React.ReactNode }) {
  const collapsed = useSidebarStore((s) => s.collapsed);
  const setCollapsed = useSidebarStore((s) => s.setCollapsed);

  return (
    <SidebarProvider
      open={!collapsed}
      onOpenChange={(open) => setCollapsed(!open)}
    >
      <AppSidebar />
      <Toaster position="top-center" />
      <SidebarInset>
        <header className="flex justify-between items-center border-b px-4 py-2">
          <SidebarTrigger />
          <div className="flex items-center gap-4">
            <UploadTenderDialog />
            <ModeToggle />
          </div>
        </header>
        <main className="h-full">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  );
}

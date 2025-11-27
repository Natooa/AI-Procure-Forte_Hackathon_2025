import React from "react";
import {
  IconChartBar,
  IconDashboard,
  IconFolder,
  IconHelp,
  IconListDetails,
  IconRobot,
  IconSearch,
  IconSettings,
  IconUpload,
  IconUsers,
} from "@tabler/icons-react";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

import { Link } from "react-router-dom";
import { toast } from "sonner";

const data = {
  navMain: [
    {
      title: "Дашборд",
      url: "/",
      icon: IconDashboard,
    },
    {
      title: "Список тендеров",
      url: "/tenders",
      icon: IconListDetails,
    },
    {
      title: "Аналитика",
      url: "#",
      icon: IconChartBar,
    },
    {
      title: "Проекты",
      url: "#",
      icon: IconFolder,
    },
    {
      title: "Команда",
      url: "#",
      icon: IconUsers,
    },
  ],
  navSecondary: [
    {
      title: "Настройки",
      url: "#",
      icon: IconSettings,
    },
    {
      title: "Получить помощь",
      url: "#",
      icon: IconHelp,
    },
    {
      title: "Поиск",
      url: "#",
      icon: IconSearch,
    },
  ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <Link to="/">
                <IconRobot className="!size-6" />
                <span className="text-lg font-bold">AI-Procure</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent className="flex flex-col gap-2">
            <SidebarMenu>
              {data.navMain.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton
                    asChild
                    tooltip={item.title}
                    onClick={(e) => {
                      if (item.url === "#") {
                        e.preventDefault();
                        toast.info("В разработке", {
                          description: "Эта страница появится позже",
                        });
                      }
                    }}
                  >
                    <Link to={item.url !== "#" ? item.url : "#"}>
                      {item.icon && <item.icon />}
                      {item.title}
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          {data.navSecondary.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton
                asChild
                tooltip={item.title}
                onClick={(e) => {
                  if (item.url === "#") {
                    e.preventDefault();
                    toast.info("В разработке", {
                      description: "Эта страница появится позже",
                    });
                  }
                }}
              >
                <Link to={item.url !== "#" ? item.url : "#"}>
                  {item.icon && <item.icon />}
                  {item.title}
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}

import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Link } from "react-router-dom";
import { AlertCircle } from "lucide-react";

export default function NotFoundPage() {
  return (
    <div className="min-h-svh flex items-center justify-center px-4">
      <Card className="w-full max-w-md shadow-xl border-0">
        <CardContent className="py-10 flex flex-col items-center text-center gap-4">
          <AlertCircle className="w-12 h-12 text-red-500 mb-2" />

          <h1 className="text-3xl font-bold">404 — Страница не найдена</h1>

          <p className="text-muted-foreground text-sm">
            Похоже, вы попали по неверному адресу. Возможно, страница была
            перемещена или удалена.
          </p>

          <Link to="/">
            <Button className="mt-4 px-6">Вернуться на главную</Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}

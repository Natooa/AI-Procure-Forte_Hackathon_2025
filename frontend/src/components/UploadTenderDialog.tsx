import React, { useState } from "react";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { IconUpload } from "@tabler/icons-react";

export function UploadTenderDialog() {
  const [uploadType, setUploadType] = useState<"link" | "file">("link");
  const [file, setFile] = useState<File | null>(null);
  const [link, setLink] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (uploadType === "link") {
      console.log("Загружаем по ссылке:", link);
    } else {
      console.log("Загружаем файл:", file);
    }
    // Тут можно добавить API-запрос
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>
          <IconUpload />
          Загрузить тендер
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Загрузить тендер</DialogTitle>
          <DialogDescription>
            Выберите способ загрузки: ссылка или файл.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="grid gap-4">
          <div className="grid gap-3">
            <Label htmlFor="upload-type">Тип загрузки</Label>
            <Select
              value={uploadType}
              onValueChange={(val) => setUploadType(val as "link" | "file")}
            >
              <SelectTrigger id="upload-type" className="w-full">
                <SelectValue placeholder="Выберите тип" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="link">Ссылка</SelectItem>
                <SelectItem value="file">Файл</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {uploadType === "link" && (
            <div className="grid gap-3">
              <Label htmlFor="link-input">Вставьте ссылку</Label>
              <Input
                id="link-input"
                placeholder="https://example.com/tenders"
                value={link}
                onChange={(e) => setLink(e.target.value)}
              />
            </div>
          )}

          {uploadType === "file" && (
            <div className="grid gap-3">
              <Label htmlFor="file-input">Выберите файл</Label>
              <Input
                id="file-input"
                type="file"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
            </div>
          )}

          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline">Отмена</Button>
            </DialogClose>
            <Button type="submit">Загрузить</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

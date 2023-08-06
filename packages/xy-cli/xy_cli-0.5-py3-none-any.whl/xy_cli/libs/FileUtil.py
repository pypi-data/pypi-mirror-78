import os
from os import walk


class FileUtil():

    def save(self, filepath, content):
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(filepath, 'w', encoding="utf-8") as f:
            f.write(content)

    def listFiles(self, template_dir):
        f = []
        for (dirpath, dirnames, filenames) in walk(template_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                name, file_extension = os.path.splitext(filename)
                is_aura = os.path.basename(os.path.dirname(dirpath)) == "aura"
                filetype = os.path.basename(dirpath) if not is_aura else "aura"
                f.append({
                    "filepath": filepath,
                    "subpath": filepath.replace(template_dir, ""),
                    "filename": filename,
                    "name": name,
                    "ext": file_extension,
                    "is_aura": is_aura,
                    "dir_name": os.path.basename(dirpath),
                    "filetype": filetype
                })
        return f

    def readFile(self, file_path):
        f = open(file_path, 'r', encoding='utf-8')
        lines = f.readlines()
        file_content = "".join(lines)
        f.close()
        return file_content

    def format(self, template_str, dict_data):
        result = template_str
        for key, value in dict_data.items():
            result = result.replace("%s" % key, str(value))
        return result

    def clone(self, template_dir, save_dir, format_data):
        template_dir = os.path.abspath(template_dir)
        abs_save_dir = os.path.abspath(save_dir)
        for f in self.listFiles(template_dir):
            print(f["filepath"])
            template_src = self.readFile(f["filepath"])
            content = self.format(template_src, format_data)
            save_file_subpath = self.format(f["subpath"], format_data)
            self.save(abs_save_dir + save_file_subpath, content)
            print(save_dir + save_file_subpath)

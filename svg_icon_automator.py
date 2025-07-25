import os
import argparse
import re
import sys
try:
    import pyperclip
except ImportError:
    print("❌ Erro: A biblioteca 'pyperclip' não está instalada.")
    print("   Por favor, instale-a executando: pip install pyperclip (ou pip3)")
    sys.exit(1)

def to_camel_case(snake_str):
    """Converte uma string de snake-case ou kebab-case para camelCase."""
    clean_str = re.sub(r'[^a-zA-Z0-9_-]', '', snake_str)
    components = clean_str.replace('-', '_').split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def create_ts_file(svg_content, icon_name, output_dir):
    """Cria o ficheiro .tsx para o ícone SVG."""
    camel_case_name = to_camel_case(icon_name)
    file_path = os.path.join(output_dir, f"{camel_case_name}.tsx")

    ts_template = f"""const {camel_case_name} = `
{svg_content.strip()}
`;

export default {camel_case_name};
"""

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(ts_template.strip())
        print(f"✅ Ficheiro de ícone criado: {file_path}")
        return True
    except IOError as e:
        print(f"❌ Erro ao criar o ficheiro {file_path}: {e}")
        return False

def update_index_file(icon_name, index_file_path):
    """Atualiza o ficheiro de índice para importar e exportar o novo ícone."""
    camel_case_name = to_camel_case(icon_name)
    
    relative_svg_path = os.path.join('@assets/svg', camel_case_name).replace('\\', '/')

    try:
        with open(index_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        last_import_index = -1
        for i, line in reversed(list(enumerate(lines))):
            if "from '@assets/svg/" in line:
                last_import_index = i
                break
        
        new_import_line = f"import {camel_case_name} from '{relative_svg_path}';\n"
        
        if new_import_line not in "".join(lines):
            if last_import_index != -1:
                lines.insert(last_import_index + 1, new_import_line)
            else:
                for i, line in reversed(list(enumerate(lines))):
                    if "from '@assets/images/" in line:
                        last_import_index = i
                        break
                if last_import_index != -1:
                    lines.insert(last_import_index + 1, f'\n{new_import_line}')
                else:
                    lines.insert(0, new_import_line)
            print(f"✅ Importação adicionada para '{camel_case_name}'.")

        export_block_end_index = -1
        for i, line in reversed(list(enumerate(lines))):
            if line.strip() == '};':
                export_block_end_index = i
                break

        if export_block_end_index != -1:
            new_export_line = f"  {camel_case_name},\n"
            
            if new_export_line not in "".join(lines):
                lines.insert(export_block_end_index, new_export_line)
                print(f"✅ Exportação adicionada para '{camel_case_name}'.")
        else:
            print("⚠️ Aviso: Bloco de exportação 'export let icons = {' não encontrado.")
            return False

        with open(index_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
        print(f"✅ Ficheiro de índice atualizado: {index_file_path}")
        return True

    except FileNotFoundError:
        print(f"❌ Erro: Ficheiro de índice não encontrado em '{index_file_path}'.")
        return False
    except IOError as e:
        print(f"❌ Erro ao ler ou escrever no ficheiro de índice: {e}")
        return False

def find_existing_svg(new_svg_content, output_dir):
    """Verifica se um SVG com o mesmo conteúdo já existe, checando ficheiros .ts e .tsx."""
    if not os.path.isdir(output_dir):
        return None

    normalized_new_content = re.sub(r'\s+', '', new_svg_content).strip()

    for filename in os.listdir(output_dir):
        if filename.endswith((".ts", ".tsx")):
            file_path = os.path.join(output_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r'`(.*)`', content, re.DOTALL)
                    if match:
                        existing_svg = match.group(1).strip()
                        normalized_existing = re.sub(r'\s+', '', existing_svg).strip()
                        if normalized_existing == normalized_new_content:
                            base_name = os.path.splitext(filename)[0]
                            return to_camel_case(base_name)
            except Exception as e:
                print(f"⚠️ Aviso: Não foi possível ler o ficheiro {filename}: {e}")
    return None


def main():
    parser = argparse.ArgumentParser(description="Automatiza a criação de constantes de ícones SVG para projetos React Native.")
    
    parser.add_argument('--output-dir', default='assets/svg', help="Diretório de saída para os ficheiros .tsx.")
    parser.add_argument('--index-file', default='src/constants/icons.ts', help="Caminho para o ficheiro de índice a ser atualizado.")
    
    args = parser.parse_args()

    try:
        icon_name = input("✏️ Digite o nome do ícone (ex: meu-novo-icone) e pressione Enter: ")
        if not icon_name.strip():
            print("❌ Erro: O nome do ícone não pode estar vazio.")
            return
    except KeyboardInterrupt:
        print("\n👋 Operação cancelada pelo utilizador.")
        return

    svg_content = pyperclip.paste()

    if not svg_content or not svg_content.strip().startswith('<svg'):
        print("❌ Erro: Nenhum conteúdo SVG válido foi encontrado na sua área de transferência.")
        print("   Por favor, copie o código SVG e tente novamente.")
        return

    existing_icon_name = find_existing_svg(svg_content, args.output_dir)
    if existing_icon_name:
        print(f"⚠️ Aviso: Este ícone já existe com o nome '{existing_icon_name}'.")
        print("   Nenhuma ação foi executada.")
        return

    if create_ts_file(svg_content, icon_name, args.output_dir):
        update_index_file(icon_name, args.index_file)

if __name__ == '__main__':
    main()
# svg_icon_automator.py
import os
import argparse
import re
import sys
# Tenta importar a biblioteca para interagir com a área de transferência
try:
    import pyperclip
except ImportError:
    print("❌ Erro: A biblioteca 'pyperclip' não está instalada.")
    print("   Por favor, instale-a executando: pip install pyperclip (ou pip3)")
    sys.exit(1)

def to_camel_case(snake_str):
    """Converte uma string de snake-case ou kebab-case para camelCase."""
    clean_str = re.sub(r'[^a-zA-Z0-9_-]', '', snake_str)
    components = clean_str.replace('-', '_').split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def create_ts_file(svg_content, icon_name, output_dir):
    """Cria o ficheiro .tsx para o ícone SVG."""
    camel_case_name = to_camel_case(icon_name)
    file_path = os.path.join(output_dir, f"{camel_case_name}.tsx")

    ts_template = f"""const {camel_case_name} = `
{svg_content.strip()}
`;

export default {camel_case_name};
"""

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(ts_template.strip())
        print(f"✅ Ficheiro de ícone criado: {file_path}")
        return True
    except IOError as e:
        print(f"❌ Erro ao criar o ficheiro {file_path}: {e}")
        return False

def update_index_file(icon_name, index_file_path):
    """Atualiza o ficheiro de índice para importar e exportar o novo ícone."""
    camel_case_name = to_camel_case(icon_name)
    
    relative_svg_path = os.path.join('@assets/svg', camel_case_name).replace('\\', '/')

    try:
        with open(index_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # --- Adiciona a nova importação ---
        last_import_index = -1
        for i, line in reversed(list(enumerate(lines))):
            if "from '@assets/svg/" in line:
                last_import_index = i
                break
        
        new_import_line = f"import {camel_case_name} from '{relative_svg_path}';\n"
        
        if new_import_line not in "".join(lines):
            if last_import_index != -1:
                lines.insert(last_import_index + 1, new_import_line)
            else:
                for i, line in reversed(list(enumerate(lines))):
                    if "from '@assets/images/" in line:
                        last_import_index = i
                        break
                if last_import_index != -1:
                    lines.insert(last_import_index + 1, f'\n{new_import_line}')
                else:
                    lines.insert(0, new_import_line)
            print(f"✅ Importação adicionada para '{camel_case_name}'.")

        # --- Adiciona a nova exportação ---
        export_block_end_index = -1
        for i, line in reversed(list(enumerate(lines))):
            if line.strip() == '};':
                export_block_end_index = i
                break

        if export_block_end_index != -1:
            new_export_line = f"  {camel_case_name},\n"
            
            if new_export_line not in "".join(lines):
                lines.insert(export_block_end_index, new_export_line)
                print(f"✅ Exportação adicionada para '{camel_case_name}'.")
        else:
            print("⚠️ Aviso: Bloco de exportação 'export let icons = {' não encontrado.")
            return False

        with open(index_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
        print(f"✅ Ficheiro de índice atualizado: {index_file_path}")
        return True

    except FileNotFoundError:
        print(f"❌ Erro: Ficheiro de índice não encontrado em '{index_file_path}'.")
        return False
    except IOError as e:
        print(f"❌ Erro ao ler ou escrever no ficheiro de índice: {e}")
        return False

def find_existing_svg(new_svg_content, output_dir):
    """Verifica se um SVG com o mesmo conteúdo já existe, checando ficheiros .ts e .tsx."""
    if not os.path.isdir(output_dir):
        return None

    normalized_new_content = re.sub(r'\s+', '', new_svg_content).strip()

    for filename in os.listdir(output_dir):
        if filename.endswith((".ts", ".tsx")):
            file_path = os.path.join(output_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r'`(.*)`', content, re.DOTALL)
                    if match:
                        existing_svg = match.group(1).strip()
                        normalized_existing = re.sub(r'\s+', '', existing_svg).strip()
                        if normalized_existing == normalized_new_content:
                            base_name = os.path.splitext(filename)[0]
                            return to_camel_case(base_name)
            except Exception as e:
                print(f"⚠️ Aviso: Não foi possível ler o ficheiro {filename}: {e}")
    return None


def main():
    parser = argparse.ArgumentParser(description="Automatiza a criação de constantes de ícones SVG para projetos React Native.")
    
    parser.add_argument('--output-dir', default='assets/svg', help="Diretório de saída para os ficheiros .tsx.")
    parser.add_argument('--index-file', default='src/constants/icons.ts', help="Caminho para o ficheiro de índice a ser atualizado.")
    
    args = parser.parse_args()

    try:
        icon_name = input("✏️ Introduza o nome do ícone (ex: meu-novo-icone) e pressione Enter: ")
        if not icon_name.strip():
            print("❌ Erro: O nome do ícone não pode estar vazio.")
            return
    except KeyboardInterrupt:
        print("\n👋 Operação cancelada pelo utilizador.")
        return

    svg_content = pyperclip.paste()

    if not svg_content or not svg_content.strip().startswith('<svg'):
        print("❌ Erro: Nenhum conteúdo SVG válido foi encontrado na sua área de transferência.")
        print("   Por favor, copie o código SVG e tente novamente.")
        return

    existing_icon_name = find_existing_svg(svg_content, args.output_dir)
    if existing_icon_name:
        print(f"⚠️ Aviso: Este ícone já existe com o nome '{existing_icon_name}'.")
        print("   Nenhuma ação foi executada.")
        return

    if create_ts_file(svg_content, icon_name, args.output_dir):
        if update_index_file(icon_name, args.index_file):
            print("\n🚀 Evoluir Juntos!")

if __name__ == '__main__':
    main()

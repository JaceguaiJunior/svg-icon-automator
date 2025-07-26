# 🛠️ Automatizador de Ícones SVG

## A Saga de um Desenvolvedor e Seus Ícones

Se a sua vida já é perfeita e você não tem tempo para as histórias do mundo real do desenvolvimento, vá direto para os [Pré-requisitos](#pré-requisitos). Mas se você gosta de uma boa história sobre como a busca pela eficiência leva à criação de soluções inteligentes, siga em frente.

Nos nossos projetos, tomamos a decisão de usar ícones SVG como constantes de string. Por quê?

* Controle total
* Tamanho final do app pequeno
* Evita bibliotecas grandes só para um ícone simples

Na prática, o fluxo de trabalho para adicionar um novo ícone envolvia:

1. Encontrar a pasta `assets/svg`
2. Criar um novo arquivo `.tsx`, como `setaBonita.tsx`
3. Copiar o SVG do Figma e colar no novo arquivo
4. Navegar até `constants/icons.ts`
5. Escrever a linha de importação correta
6. Incluir no objeto `icons`

Esse processo, repetido várias vezes, consumia tempo e facilitava erros, como duplicação de ícones com nomes diferentes.

Este script foi criado para automatizar esse fluxo, garantir consistência e agilidade no dia a dia. Ele verifica se o SVG já existe, cria o arquivo `.ts`, adiciona a linha de importação e insere o novo ícone no objeto `icons`.

---

## ✅ Pré-requisitos

* **Python 3**
  Verifique com:

  ```bash
  python3 --version
  ```

* **Biblioteca pyperclip**
  Instale com:

  ```bash
  pip3 install pyperclip
  ```

---

## 📁 Estrutura de Pastas Esperada

```
.
├── assets/
│   └── svg/
│       ├── meuIcone.tsx
│       └── outroIcone.tsx
│
└── src/
    └── constants/
        └── icons.ts
```

Se sua estrutura for diferente, você pode editar os caminhos no script.

---

## 🚀 Como Usar

1. Copie o SVG completo da área de design (ex: Figma)

2. No terminal, execute:

   ```bash
   python3 svg_icon_automator.py
   ```

3. Digite o nome do ícone (ex: `meu-icone-novo`) e pressione **Enter**

O script irá:

* Criar o arquivo `assets/svg/meuIconeNovo.tsx`
* Adicionar o `import` e o uso no `constants/icons.ts`
* Exibir mensagens de sucesso no terminal

---

## 🧪 Exemplo de Uso

### Componente `Icon.tsx`

```tsx
import { SvgXml } from 'react-native-svg';
import { View } from 'react-native';

interface IIcon {
  iconName?: string;
  fill?: string;
}

function Icon({ iconName, fill }: IIcon) {
  const replaceFillColor = (svgString: string, color: string | undefined) => {
    if (!color) return svgString;

    return svgString.replace(/fill="([^"]+)"/g, `fill="${color}"`);
  };

  const svgWithNewColor = iconName ? replaceFillColor(iconName, fill) : '';

  return (
    <View>
      {iconName && iconName.length > 0 && <SvgXml xml={svgWithNewColor} />}
    </View>
  );
}

export default Icon;
```
---

## 🔗 `icons.ts` (Exemplo)


```ts
import alertSuggestion from '@assets/svg/alertSuggestion';
import arrowDown from '@assets/svg/arrowDown';
// outros ícones
import meuIconeNovo from '@assets/svg/meuIconeNovo'; // <-- Linha adicionada pelo script

export const icons = {
  alertSuggestion,
  arrowDown,
  meuIconeNovo, // <-- Linha adicionada pelo script
};
```
---

## 🔗 Como usar:

```tsx
import { icons } from '@constants/icons';

<Icon iconName={icons.meuIconeNovo} />
```


## 🤝 Contribuindo

Contribuições são bem-vindas! Caso queira colaborar com melhorias ou correções, basta abrir um Pull Request.

---

🚀 Que este script torne seu fluxo com SVGs mais eficiente! Evoluir Juntos!

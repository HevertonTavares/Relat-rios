# Gerador de Relatórios PDF - Appmax

Este projeto permite gerar relatórios mensais em PDF para múltiplas lojas a partir de uma planilha no formato `.xlsx`, com visual estruturado e identidade visual da Appmax.

## Funcionalidades
- Geração de um PDF por loja com base em dados da planilha
- Layout visual aprovado com fundo roxo, textos brancos e blocos destacados
- Gráfico de pizza com participação dos meios de pagamento (Cartão, Pix, Boleto)
- Bloco de recuperação de vendas com valores detalhados
- Inclusão da logo da Appmax no rodapé direito de cada página

## Como usar
1. Coloque o arquivo `Appmax.png` (logo) na mesma pasta do projeto
2. Suba a aplicação com o Streamlit:

```bash
streamlit run app.py
```

3. Faça upload da planilha `.xlsx`
4. Baixe os relatórios individuais gerados para cada loja

## Dependências
- Streamlit
- FPDF
- Matplotlib
- Pandas

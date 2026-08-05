#!/usr/bin/env bash
# ==============================================================================
# setup_data.sh — Download do dataset Olist (Brazilian E-Commerce)
# ==============================================================================
# Uso:
#   ./setup_data.sh
#
# Este script baixa o dataset público da Olist do Kaggle e o extrai na pasta
# data/olist/. Ele tenta usar a Kaggle CLI primeiro; se não estiver disponível,
# oferece instruções para download manual.
#
# Flags:
#   --force    Sobrescreve o dataset mesmo se já existir
#
# Pré-requisitos (para download automático):
#   1. pip install kaggle
#   2. Configure suas credenciais em ~/.kaggle/kaggle.json
#      (Obtenha em: https://www.kaggle.com/settings → API → Create New Token)
# ==============================================================================

set -euo pipefail

FORCE=false
for arg in "$@"; do
    case "$arg" in
        --force|-f) FORCE=true ;;
    esac
done

DATASET_SLUG="olistbr/brazilian-ecommerce"
DATA_DIR="$(cd "$(dirname "$0")" && pwd)/data/olist"
ZIP_PATH="$(cd "$(dirname "$0")" && pwd)/data/brazilian-ecommerce.zip"

EXPECTED_FILES=(
    "olist_customers_dataset.csv"
    "olist_orders_dataset.csv"
    "olist_order_items_dataset.csv"
    "olist_order_payments_dataset.csv"
    "olist_order_reviews_dataset.csv"
    "olist_products_dataset.csv"
    "olist_sellers_dataset.csv"
    "olist_geolocation_dataset.csv"
    "product_category_name_translation.csv"
)

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  📦 Setup do Dataset Olist — Brazilian E-Commerce${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════${NC}"
    echo ""
}

check_existing_data() {
    local count=0
    for f in "${EXPECTED_FILES[@]}"; do
        if [[ -f "$DATA_DIR/$f" ]]; then
            count=$((count + 1))
        fi
    done

    if [[ $count -eq ${#EXPECTED_FILES[@]} ]]; then
        echo -e "${GREEN}✅ Dataset já está completo em ${DATA_DIR}/${NC}"
        echo -e "   Arquivos encontrados: ${count}/${#EXPECTED_FILES[@]}"
        if [[ "$FORCE" == false ]]; then
            echo -e "${GREEN}Nada a fazer. Use ${YELLOW}--force${GREEN} para baixar novamente.${NC}"
            exit 0
        fi
        echo -e "${YELLOW}⚠️  Flag --force detectada. Baixando novamente...${NC}"
    elif [[ $count -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  Dataset parcialmente presente (${count}/${#EXPECTED_FILES[@]} arquivos)${NC}"
        echo "   Continuando com o download..."
    else
        echo -e "${YELLOW}📂 Dataset não encontrado. Iniciando download...${NC}"
    fi
}

download_via_kaggle_cli() {
    echo -e "${BLUE}🔍 Verificando Kaggle CLI...${NC}"

    if command -v kaggle &>/dev/null; then
        echo -e "${GREEN}✅ Kaggle CLI encontrada: $(kaggle --version 2>&1 | head -1)${NC}"
    elif python3 -m kaggle --version &>/dev/null 2>&1; then
        echo -e "${GREEN}✅ Kaggle CLI encontrada via python3 -m kaggle${NC}"
        kaggle() { python3 -m kaggle "$@"; }
    else
        return 1
    fi

    # Verificar credenciais
    if [[ ! -f "$HOME/.kaggle/kaggle.json" ]]; then
        echo -e "${RED}❌ Credenciais do Kaggle não encontradas em ~/.kaggle/kaggle.json${NC}"
        return 1
    fi

    echo -e "${BLUE}⬇️  Baixando dataset '${DATASET_SLUG}' via Kaggle CLI...${NC}"
    mkdir -p "$DATA_DIR"

    kaggle datasets download -d "$DATASET_SLUG" -p "$(dirname "$DATA_DIR")" --unzip --force

    # O kaggle pode extrair direto no diretório pai — mover se necessário
    for f in "${EXPECTED_FILES[@]}"; do
        if [[ -f "$(dirname "$DATA_DIR")/$f" && ! -f "$DATA_DIR/$f" ]]; then
            mv "$(dirname "$DATA_DIR")/$f" "$DATA_DIR/"
        fi
    done

    return 0
}

download_via_python() {
    echo -e "${BLUE}🔍 Tentando download via Python (kaggle API)...${NC}"

    python3 - <<'PYEOF'
import sys
try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    print("✅ Kaggle API autenticada com sucesso")
except Exception as e:
    print(f"❌ Falha na autenticação: {e}", file=sys.stderr)
    sys.exit(1)

import os
data_dir = os.environ.get("DATA_DIR", "data/olist")
parent_dir = os.path.dirname(data_dir)
os.makedirs(data_dir, exist_ok=True)

print(f"⬇️  Baixando dataset para {parent_dir}...")
api.dataset_download_files("olistbr/brazilian-ecommerce", path=parent_dir, unzip=True, force=True)

# Mover arquivos se extraídos no diretório pai
expected = [
    "olist_customers_dataset.csv", "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv", "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv", "olist_products_dataset.csv",
    "olist_sellers_dataset.csv", "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv"
]
for f in expected:
    src = os.path.join(parent_dir, f)
    dst = os.path.join(data_dir, f)
    if os.path.exists(src) and not os.path.exists(dst):
        os.rename(src, dst)

print("✅ Download concluído!")
PYEOF
}

show_manual_instructions() {
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  📋 INSTRUÇÕES PARA DOWNLOAD MANUAL${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${BLUE}Opção 1: Instalar e configurar Kaggle CLI${NC}"
    echo "  ────────────────────────────────────────"
    echo "  1. pip install kaggle"
    echo "  2. Acesse: https://www.kaggle.com/settings"
    echo "     → Seção 'API' → Clique 'Create New Token'"
    echo "  3. Salve o arquivo kaggle.json em ~/.kaggle/"
    echo "     chmod 600 ~/.kaggle/kaggle.json"
    echo "  4. Execute este script novamente: ./setup_data.sh"
    echo ""
    echo -e "  ${BLUE}Opção 2: Download manual pelo navegador${NC}"
    echo "  ────────────────────────────────────────"
    echo "  1. Acesse: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce"
    echo "  2. Clique em 'Download' (necessário conta Kaggle gratuita)"
    echo "  3. Extraia o ZIP na pasta: ${DATA_DIR}/"
    echo ""
    echo -e "  ${BLUE}Opção 3: Via curl (requer autenticação Kaggle)${NC}"
    echo "  ────────────────────────────────────────"
    echo "  mkdir -p ${DATA_DIR}"
    echo "  kaggle datasets download -d olistbr/brazilian-ecommerce -p data/ --unzip"
    echo "  mv data/*.csv ${DATA_DIR}/"
    echo ""
    echo -e "  ${YELLOW}Após o download, a pasta data/olist/ deve conter 9 arquivos CSV.${NC}"
    echo ""
}

verify_download() {
    echo ""
    echo -e "${BLUE}🔎 Verificando integridade do dataset...${NC}"

    local missing=0
    for f in "${EXPECTED_FILES[@]}"; do
        if [[ -f "$DATA_DIR/$f" ]]; then
            local size
            size=$(du -h "$DATA_DIR/$f" | cut -f1)
            echo -e "  ${GREEN}✅ $f ${NC}(${size})"
        else
            echo -e "  ${RED}❌ $f — AUSENTE${NC}"
            ((missing++))
        fi
    done

    echo ""
    if [[ $missing -eq 0 ]]; then
        echo -e "${GREEN}══════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  ✅ Dataset completo! ${#EXPECTED_FILES[@]}/${#EXPECTED_FILES[@]} arquivos presentes.${NC}"
        echo -e "${GREEN}  📂 Local: ${DATA_DIR}/${NC}"
        echo -e "${GREEN}══════════════════════════════════════════════════════════${NC}"
    else
        echo -e "${RED}⚠️  ${missing} arquivo(s) ausente(s). Verifique o download.${NC}"
        exit 1
    fi
}

# Limpar zip residual
cleanup() {
    if [[ -f "$ZIP_PATH" ]]; then
        rm -f "$ZIP_PATH"
        echo -e "${BLUE}🧹 ZIP temporário removido.${NC}"
    fi
}

# ==============================================================================
# Main
# ==============================================================================
print_header
check_existing_data

# Tentar download automático (CLI > Python > Manual)
if download_via_kaggle_cli 2>/dev/null; then
    echo -e "${GREEN}✅ Download via Kaggle CLI bem-sucedido!${NC}"
elif DATA_DIR="$DATA_DIR" download_via_python 2>/dev/null; then
    echo -e "${GREEN}✅ Download via Python API bem-sucedido!${NC}"
else
    echo -e "${YELLOW}⚠️  Download automático não disponível.${NC}"
    show_manual_instructions
    exit 1
fi

cleanup
verify_download

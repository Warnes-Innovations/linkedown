# Copyright (c) 2026 Gregory R. Warnes
# SPDX-License-Identifier: MIT
"""linkedown — Bidirectional Markdown ↔ LinkedIn Unicode converter."""

from .li_to_md import linkedin_to_md
from .md_to_li import md_to_linkedin

__all__ = ["md_to_linkedin", "linkedin_to_md"]
__version__ = "0.1.0"

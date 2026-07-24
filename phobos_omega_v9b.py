#!/usr/bin/env python3
# PHOBOS-Ω v9.1 "NOIR" - Memetic Flyer Control + Diffusion Prompt Generator (ENHANCED)
# Intègre: sélection granulaire des éléments textuels + génération de prompts pour IA diffusion
# v9.1: Descriptions textuelles des symboles dans les prompts (plus de codes ASCII)
# ASCII Pur + Unicode Escapes (Bulletproof pour eLive)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random, os, json, math, tempfile
from datetime import datetime
from collections import deque
import threading

# ====================== FALLBACKS ASCII (UNICODE ESCAPES) ======================
# Pour l'affichage Tkinter uniquement

VON_PETZINGER_ASCII = {
    "\u25B3": "[TRI]", "\u25AB": "[SQR]", "\u29C6": "[CUBE]", "\u29C8": "[BOX]",
    "\u2A00": "[CIR]", "\u26F6": "[FRAME]", "\u2B20": "[PENT]", "\u2B21": "[HEX]",
    "\u2B22": "[HEX2]", "\u2BC1": "[SEPT]", "\u2332": "[ARROW]", "\u29C9": "[DBOX]",
    "\u29BB": "[CROSS]", "\u233E": "[RING]", "\u233D": "[HALF]", "\u233C": "[GRID]",
    "\u233A": "[MESH]", "\u233B": "[NET]", "\u2330": "[PIPE]", "\u2A2F": "[X]",
    "\u29D6": "[HOUR]", "\u29D7": "[TIME]", "\u29D8": "[FLOW]", "\u29D9": "[WAVE]",
    "\u29DA": "[SPIRAL]", "\u29DB": "[VORTEX]"
}

FUTHARK_ASCII = {
    "\u16A0": "F", "\u16A2": "U", "\u16A6": "TH", "\u16A8": "A", "\u16B1": "R",
    "\u16B2": "K", "\u16B7": "G", "\u16B9": "W", "\u16BA": "H", "\u16BE": "N",
    "\u16C1": "I", "\u16C3": "J", "\u16C7": "EO", "\u16C8": "P", "\u16C9": "Z",
    "\u16CB": "S", "\u16CF": "T", "\u16D2": "B", "\u16D6": "E", "\u16D7": "M",
    "\u16DA": "L", "\u16DC": "NG", "\u16DF": "O", "\u16DE": "D", "\u16A3": "YR",
    "\u16E1": "IA", "\u16E0": "EA"
}


def safe_symbol(symbol, fallback_dict):
    if not symbol:
        return "?"
    if any(ord(c) > 127 for c in symbol):
        return fallback_dict.get(symbol, "[RUNE]")
    return symbol


# ====================== DESCRIPTIONS POUR PROMPTS DIFFUSION (NOUVEAU v9.1) ======================
# Descriptions textuelles en anglais pour les modèles de diffusion
# Ces descriptions remplacent les codes ASCII dans les prompts

SYMBOL_DESCRIPTIONS = {
    "[TRI]": "triangle symbol, three-pointed geometric shape",
    "[SQR]": "square symbol, four-sided geometric shape",
    "[CUBE]": "cube symbol, three-dimensional box shape",
    "[BOX]": "box symbol, rectangular container shape",
    "[CIR]": "circle symbol with dot in center, solar symbol",
    "[FRAME]": "framed square, bordered rectangle symbol",
    "[PENT]": "pentagram symbol, five-pointed star",
    "[HEX]": "hexagram symbol, six-pointed star",
    "[HEX2]": "hexagon symbol, six-sided geometric shape",
    "[SEPT]": "heptagram symbol, seven-pointed star",
    "[ARROW]": "arrow symbol, directional pointer",
    "[DBOX]": "double box symbol, nested rectangles",
    "[CROSS]": "crossed circle symbol, target-like mark",
    "[RING]": "ring symbol, circular band",
    "[HALF]": "half-circle symbol, semicircle shape",
    "[GRID]": "grid symbol, matrix of intersecting lines",
    "[MESH]": "mesh symbol, net-like pattern",
    "[NET]": "net symbol, woven pattern",
    "[PIPE]": "pipe symbol, vertical line with branches",
    "[X]": "X symbol, crossed lines mark",
    "[HOUR]": "hourglass symbol, time measurement shape",
    "[TIME]": "clock symbol, circular time indicator",
    "[FLOW]": "flow symbol, directional wave pattern",
    "[WAVE]": "wave symbol, undulating line pattern",
    "[SPIRAL]": "spiral symbol, coiling curve pattern",
    "[VORTEX]": "vortex symbol, swirling funnel shape"
}

RUNE_DESCRIPTIONS = {
    "F": "Fehu rune, cattle wealth symbol from Elder Futhark",
    "U": "Uruz rune, aurochs strength symbol from Elder Futhark",
    "TH": "Thurisaz rune, thorn/giant symbol from Elder Futhark",
    "A": "Ansuz rune, divine mouth/speech symbol from Elder Futhark",
    "R": "Raido rune, journey/riding symbol from Elder Futhark",
    "K": "Kenaz rune, torch/fire symbol from Elder Futhark",
    "G": "Gebo rune, gift/partnership symbol from Elder Futhark",
    "W": "Wunjo rune, joy/bliss symbol from Elder Futhark",
    "H": "Hagalaz rune, hail/destruction symbol from Elder Futhark",
    "N": "Nauthiz rune, need/constraint symbol from Elder Futhark",
    "I": "Isa rune, ice/stillness symbol from Elder Futhark",
    "J": "Jera rune, harvest/year symbol from Elder Futhark",
    "EO": "Eihwaz rune, yew tree/defense symbol from Elder Futhark",
    "P": "Perthro rune, mystery/fate symbol from Elder Futhark",
    "Z": "Algiz rune, protection/elk symbol from Elder Futhark",
    "S": "Sowilo rune, sun/victory symbol from Elder Futhark",
    "T": "Tiwaz rune, justice/sky god symbol from Elder Futhark",
    "B": "Berkana rune, birch/growth symbol from Elder Futhark",
    "E": "Ehwaz rune, horse/movement symbol from Elder Futhark",
    "M": "Mannaz rune, humanity/self symbol from Elder Futhark",
    "L": "Laguz rune, water/flow symbol from Elder Futhark",
    "NG": "Ingwaz rune, fertility/seed symbol from Elder Futhark",
    "O": "Othala rune, heritage/estate symbol from Elder Futhark",
    "D": "Dagaz rune, dawn/breakthrough symbol from Elder Futhark",
    "YR": "Yr rune, bow/yew symbol from Elder Futhark",
    "IA": "Ior rune, eel/ambiguity symbol from Elder Futhark",
    "EA": "Ear rune, grave/earth symbol from Elder Futhark"
}

ARCHETYPE_DESCRIPTIONS = {
    "L'Ombre": "The Shadow, Jungian archetype of the repressed self",
    "L'Anima": "The Anima, Jungian archetype of the feminine inner self",
    "L'Animus": "The Animus, Jungian archetype of the masculine inner self",
    "Le Vieillard Sage": "The Wise Old Man, Jungian archetype of the mentor",
    "La Grande Mère": "The Great Mother, Jungian archetype of nurturing and creation",
    "Le Héros": "The Hero, Jungian archetype of courage and quest",
    "Le Trickster": "The Trickster, Jungian archetype of chaos and paradox",
    "Le Puer Aeternus": "The Puer Aeternus, Jungian archetype of the eternal youth",
    "Le Démon": "The Demon, Jungian archetype of the destructive shadow",
    "Le Self": "The Self, Jungian archetype of the total psyche",
    "Le Sage Fou": "The Fool, Jungian archetype of innocence and potential",
    "L'Enfant Divin": "The Divine Child, Jungian archetype of rebirth and hope",
    "L'Étranger": "The Stranger, Jungian archetype of the outsider"
}

EFFECT_DESCRIPTIONS = {
    "boucle mémétique": "memetic loop, self-replicating idea cycle",
    "résonance subliminale": "subliminal resonance, hidden frequency effect",
    "activation transhistorique": "transhistorical activation, cross-era trigger",
    "déclenchement onirique": "oneiric trigger, dream-state activation",
    "infiltration symbolique": "symbolic infiltration, gradual meaning渗透",
    "résonance archétypale": "archetypal resonance, deep pattern recognition",
    "bascule ontologique": "ontological shift, reality perception flip",
    "effet miroir récursif": "recursive mirror effect, self-reflecting loop",
    "dérivation narrative": "narrative derivation, story-based distortion",
    "alignement cosmique": "cosmic alignment, universal pattern sync",
    "glissement sémantique": "semantic drift, meaning shift over time",
    "renaissance symbolique": "symbolic rebirth, meaning renewal",
    "décentrage perceptif": "perceptual decentring, viewpoint shift"
}


# ====================== CONFIGURATION DU FLYER ======================

class FlyerConfig:
    def __init__(self):
        self.show_title = True
        self.show_von_petzinger = True
        self.show_futhark = True
        self.show_archetype = True
        self.show_effect = True
        self.show_dna = True
        self.show_philosophical = True
        self.show_footer = True
        self.diffusion_style = "glitch_art"
        self.diffusion_quality = "high"


# ====================== GÉNÉRATEUR DE PROMPTS DIFFUSION (v9.1 ENHANCED) ======================

class DiffusionPromptGenerator:
    STYLES = {
        "glitch_art": {
            "name": "Glitch Art Cyberpunk",
            "base": "cyberpunk glitch art poster, digital corruption, scanlines, chromatic aberration, neon colors on dark background",
            "modifiers": ["VHS distortion", "pixel sorting", "data moshing", "CRT monitor effect", "RGB split"],
            "quality": "8k resolution, highly detailed, sharp focus",
            "negative": "blurry, low quality, watermark, text artifacts"
        },
        "vintage": {
            "name": "Vintage Poster Aged",
            "base": "vintage occult poster, aged paper texture, faded colors, worn edges, retro typography",
            "modifiers": ["coffee stains", "fold marks", "yellowed paper", "vintage print quality", "retro color palette"],
            "quality": "high resolution, detailed texture, authentic vintage look",
            "negative": "modern, digital, clean, pristine"
        },
        "occult": {
            "name": "Occult Manuscript",
            "base": "ancient occult manuscript page, mystical symbols, parchment texture, esoteric diagram",
            "modifiers": ["hand-drawn symbols", "alchemical ink", "mystical glow", "sacred geometry", "ancient wisdom"],
            "quality": "ultra detailed, intricate patterns, mystical atmosphere",
            "negative": "modern, digital, cartoon, simplistic"
        },
        "neon": {
            "name": "Neon Noir",
            "base": "neon noir poster, glowing symbols on black background, cyberpunk aesthetic, dark atmosphere",
            "modifiers": ["neon glow effect", "light trails", "dark urban background", "futuristic typography", "electric colors"],
            "quality": "8k, vibrant colors, high contrast, sharp details",
            "negative": "dull colors, low contrast, blurry, amateur"
        },
        "minimalist": {
            "name": "Minimalist Design",
            "base": "minimalist poster design, clean layout, modern typography, simple geometric shapes",
            "modifiers": ["white space", "clean lines", "modern aesthetic", "subtle gradients", "elegant composition"],
            "quality": "high resolution, professional design, crisp edges",
            "negative": "cluttered, busy, ornate, decorative"
        }
    }
    
    @staticmethod
    def generate_prompt(dna, triptych, config, palette_name):
        style = DiffusionPromptGenerator.STYLES.get(config.diffusion_style, DiffusionPromptGenerator.STYLES["glitch_art"])
        glyph_desc = DiffusionPromptGenerator._describe_glyph(dna, palette_name)
        text_elements = DiffusionPromptGenerator._build_text_elements_v91(triptych, dna, config)
        
        prompt_parts = [
            f"{style['name']} poster design",
            style['base'],
            f"central glyph: {glyph_desc}",
        ]
        
        if text_elements:
            prompt_parts.append(f"visual elements: {text_elements}")
        
        selected_modifiers = random.sample(style['modifiers'], min(3, len(style['modifiers'])))
        prompt_parts.append(", ".join(selected_modifiers))
        prompt_parts.append(style['quality'])
        
        prompt = ", ".join(prompt_parts)
        negative_prompt = style['negative']
        
        return {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "style": style['name'],
            "parameters": {
                "aspect_ratio": "9:16",
                "seed": str(abs(hash(dna.seed)) % 1000000),
                "cfg_scale": "7-9",
                "steps": "30-50"
            }
        }
    
    @staticmethod
    def _describe_glyph(dna, palette_name):
        symmetry_desc = {
            3: "triangular symmetry", 4: "square symmetry", 5: "pentagonal symmetry",
            6: "hexagonal symmetry", 7: "heptagonal symmetry", 8: "octagonal symmetry",
            9: "nonagonal symmetry", 12: "dodecagonal symmetry"
        }
        complexity_desc = "simple" if dna.complexity < 0.5 else "moderate" if dna.complexity < 0.8 else "highly complex"
        palette_colors = {
            "phobos_classic": "pink, green, purple, cyan, yellow",
            "void_depths": "dark purple, deep violet, black",
            "solar_flare": "orange, yellow, gold",
            "quantum_foam": "cyan, teal, blue",
            "blood_moon": "red, crimson, magenta",
            "hyperdelic": "magenta, cyan, yellow, pink",
            "arctic_aurora": "cyan, blue, white",
            "toxic_dream": "green, lime, yellow",
            "paleo_ochre": "brown, ochre, gold",
            "cave_shadow": "gray, black, dark tones"
        }
        return (
            f"{complexity_desc} concentric rings with "
            f"{symmetry_desc.get(dna.symmetry, 'radial')} symmetry, "
            f"colors: {palette_colors.get(palette_name, 'multicolor')}, "
            f"glowing center, mandala-like pattern"
        )
    
    @staticmethod
    def _build_text_elements_v91(triptych, dna, config):
        """v9.1: Utilise les descriptions textuelles au lieu des codes ASCII"""
        elements = []
        
        if config.show_title:
            elements.append("title text: PHOBOS-OMEGA v9.1 NOIR in bold futuristic typography")
        
        if config.show_von_petzinger and triptych:
            vp = safe_symbol(triptych.get('von_petzinger', '?'), VON_PETZINGER_ASCII)
            vp_desc = SYMBOL_DESCRIPTIONS.get(vp, f"mysterious geometric symbol labeled {vp}")
            elements.append(f"central symbol: {vp_desc}")
        
        if config.show_futhark and triptych:
            futh = safe_symbol(triptych.get('futhark', '?'), FUTHARK_ASCII)
            rune_desc = RUNE_DESCRIPTIONS.get(futh, f"Elder Futhark rune '{futh}'")
            elements.append(f"runic element: {rune_desc}")
        
        if config.show_archetype and triptych:
            arch = triptych.get('jungian_archetype', '')
            arch_desc = ARCHETYPE_DESCRIPTIONS.get(arch, f"Jungian archetype '{arch}'")
            elements.append(f"archetypal theme: {arch_desc}")
        
        if config.show_effect and triptych:
            effect = triptych.get('mnemo_effect', '')
            effect_desc = EFFECT_DESCRIPTIONS.get(effect, f"memetic effect '{effect}'")
            elements.append(f"memetic effect: {effect_desc}")
        
        if config.show_dna:
            elements.append(f"DNA code number: {abs(hash(dna.seed)) % 1000000:06d}")
        
        if config.show_philosophical:
            msg = random.choice(PHILOSOPHICAL_STATEMENTS).split('\n')[0]
            elements.append(f"philosophical quote: \"{msg}\"")
        
        if config.show_footer:
            if triptych and triptych.get('id') == 999:
                elements.append("footer warning text: SCANNING OBSERVER... BIASES DETECTED... NO EXIT in red")
            else:
                elements.append("footer status text: Zero Hazard - Full Spectrum - Meta-Stable - Biased")
        
        return "; ".join(elements) if elements else "no text elements"
    
    @staticmethod
    def format_prompt_for_copy(prompt_data):
        output = []
        output.append("=" * 60)
        output.append(f"  DIFFUSION PROMPT - {prompt_data['style']}")
        output.append("=" * 60)
        output.append("")
        output.append("POSITIVE PROMPT:")
        output.append("-" * 60)
        output.append(prompt_data['prompt'])
        output.append("")
        output.append("NEGATIVE PROMPT:")
        output.append("-" * 60)
        output.append(prompt_data['negative_prompt'])
        output.append("")
        output.append("PARAMETERS:")
        output.append("-" * 60)
        for key, value in prompt_data['parameters'].items():
            output.append(f"  {key}: {value}")
        output.append("")
        output.append("=" * 60)
        return "\n".join(output)


# ====================== ARCHITECTURE NEURALE ======================

class MemePalette:
    PALETTES = {
        "phobos_classic": ["#ff3366", "#33ff99", "#cc33ff", "#33ccff", "#ffff66"],
        "void_depths":    ["#0a0014", "#1a0028", "#2d0050", "#4a007a", "#6600aa"],
        "solar_flare":    ["#ff6b00", "#ff8c00", "#ffa500", "#ffc700", "#ffe900"],
        "quantum_foam":   ["#00ffaa", "#00ffdd", "#00ddff", "#00aaff", "#0088ff"],
        "blood_moon":     ["#8b0000", "#b22222", "#dc143c", "#ff1493", "#ff69b4"],
        "hyperdelic":     ["#ff00ff", "#00ffff", "#ffff00", "#ff0080", "#80ff00"],
        "arctic_aurora":  ["#00fff7", "#00d9ff", "#00b3ff", "#008dff", "#0067ff"],
        "toxic_dream":    ["#39ff14", "#7fff00", "#adff2f", "#ccff00", "#dfff00"],
        "paleo_ochre":    ["#8b4513", "#a0522d", "#cd853f", "#daa520", "#b8860b"],
        "cave_shadow":    ["#1a1a1a", "#2f2f2f", "#4a4a4a", "#696969", "#808080"]
    }

    @staticmethod
    def get_palette(name="phobos_classic"):
        return MemePalette.PALETTES.get(name, MemePalette.PALETTES["phobos_classic"])


class GlyphDNA:
    def __init__(self, seed=None):
        self.seed = seed or random.random()
        self.rng = random.Random(self.seed)
        self.complexity = self.rng.uniform(0.3, 1.0)
        self.symmetry = self.rng.choice([3, 4, 5, 6, 7, 8, 9, 12])
        self.resonance = self.rng.uniform(0.2, 0.9)
        self.mutation_rate = self.rng.uniform(0.05, 0.25)
        self.dimensional_phase = self.rng.uniform(0, 2 * math.pi)
        self.archetype_anchor = None
        self.triptych_id = None

    def mutate(self, intensity=0.1):
        self.complexity = max(0.2, min(1.0, self.complexity + self.rng.uniform(-intensity, intensity)))
        self.resonance = max(0.1, min(1.0, self.resonance + self.rng.uniform(-intensity, intensity)))
        self.dimensional_phase = (self.dimensional_phase + self.rng.uniform(-0.3, 0.3)) % (2 * math.pi)
        return self


class HyperdimensionalGlyphGenerator:
    @staticmethod
    def generate_mandala_core(draw, center, radius, dna, palette):
        layers = int(5 + dna.complexity * 10)
        for i in range(layers):
            r = radius * (1 - i / layers) * dna.resonance
            opacity = int(255 * (1 - i / layers) * 0.7)
            color = random.choice(palette)
            rgb = tuple(int(color[j:j+2], 16) for j in (1, 3, 5))
            color_with_alpha = rgb + (opacity,)
            offset_x = math.cos(dna.dimensional_phase + i * 0.3) * 5
            offset_y = math.sin(dna.dimensional_phase + i * 0.3) * 5
            draw.ellipse(
                [center[0] - r + offset_x, center[1] - r + offset_y,
                 center[0] + r + offset_x, center[1] + r + offset_y],
                outline=color_with_alpha, width=int(3 + dna.complexity * 5)
            )

    @staticmethod
    def generate_radial_arms(draw, center, max_radius, dna, palette):
        num_arms = dna.symmetry
        for arm in range(num_arms):
            angle = (arm / num_arms) * 2 * math.pi + dna.dimensional_phase
            points = []
            segments = int(20 + dna.complexity * 30)
            for t in range(segments):
                t_norm = t / segments
                r = max_radius * t_norm * dna.resonance
                noise = math.sin(t_norm * 10 + dna.seed * 100) * 20 * dna.mutation_rate
                x = center[0] + (r + noise) * math.cos(angle)
                y = center[1] + (r + noise) * math.sin(angle)
                points.append((x, y))
            if len(points) > 1:
                color = random.choice(palette)
                rgb = tuple(int(color[j:j+2], 16) for j in (1, 3, 5))
                draw.line(points, fill=rgb + (200,), width=int(2 + dna.complexity * 4))

    @staticmethod
    def generate_interference_pattern(draw, center, radius, dna, palette):
        rings = int(8 + dna.complexity * 15)
        for i in range(rings):
            r = radius * (0.3 + 0.7 * i / rings)
            phase_shift = i * 0.5 + dna.dimensional_phase
            amplitude = 15 * dna.resonance * math.sin(phase_shift)
            points = []
            segments = 120
            for seg in range(segments + 1):
                angle = (seg / segments) * 2 * math.pi
                wave = amplitude * math.sin(angle * dna.symmetry + phase_shift)
                x = center[0] + (r + wave) * math.cos(angle)
                y = center[1] + (r + wave) * math.sin(angle)
                points.append((x, y))
            color = palette[i % len(palette)]
            rgb = tuple(int(color[j:j+2], 16) for j in (1, 3, 5))
            opacity = int(120 + 100 * (1 - i / rings))
            draw.line(points + [points[0]], fill=rgb + (opacity,), width=2)

    @staticmethod
    def generate_hyperbolic_spiral(draw, center, max_radius, dna, palette):
        spirals = dna.symmetry
        for s in range(spirals):
            points = []
            angle_offset = (s / spirals) * 2 * math.pi
            t_max = 5 + dna.complexity * 10
            steps = int(100 + dna.complexity * 200)
            for i in range(steps):
                t = (i / steps) * t_max
                r = max_radius * (1 - math.exp(-t * 0.3)) * dna.resonance
                angle = t * math.pi + angle_offset + dna.dimensional_phase
                x = center[0] + r * math.cos(angle)
                y = center[1] + r * math.sin(angle)
                points.append((x, y))
            if len(points) > 1:
                color = palette[s % len(palette)]
                rgb = tuple(int(color[j:j+2], 16) for j in (1, 3, 5))
                draw.line(points, fill=rgb + (180,), width=3)

    @staticmethod
    def generate_glyph(width=1200, height=1200, dna=None, palette_name="phobos_classic"):
        if dna is None:
            dna = GlyphDNA()
        palette = MemePalette.get_palette(palette_name)
        img = Image.new('RGBA', (width, height), (10, 10, 26, 255))
        draw = ImageDraw.Draw(img, 'RGBA')
        center = (width // 2, height // 2)
        max_radius = min(width, height) * 0.4

        HyperdimensionalGlyphGenerator.generate_interference_pattern(draw, center, max_radius, dna, palette)
        HyperdimensionalGlyphGenerator.generate_hyperbolic_spiral(draw, center, max_radius, dna, palette)
        HyperdimensionalGlyphGenerator.generate_radial_arms(draw, center, max_radius, dna, palette)
        HyperdimensionalGlyphGenerator.generate_mandala_core(draw, center, max_radius * 0.3, dna, palette)

        core_color = random.choice(palette)
        rgb = tuple(int(core_color[j:j+2], 16) for j in (1, 3, 5))
        for i in range(5, 0, -1):
            opacity = int(255 * (i / 5) * 0.8)
            draw.ellipse(
                [center[0] - i*5, center[1] - i*5, center[0] + i*5, center[1] + i*5],
                fill=rgb + (opacity,)
            )

        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)
        return img, dna


# ====================== PALEO-MNEMOS ENGINE ======================

class PaleoMnemosEngine:
    def __init__(self, lexicon_path="paleo_mnemos_lexicon.json"):
        self.entries = []
        self.by_archetype = {}
        self.by_effect = {}
        self.by_symbol = {}
        self.archetypes = []
        self.effects = []
        self.symbols = []

        try:
            with open(lexicon_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            raw_entries = data.get('entries', data.get('entries ', []))
            for entry in raw_entries:
                cleaned = {k.strip(): v for k, v in entry.items()}
                self.entries.append(cleaned)

            for entry in self.entries:
                arch = entry.get('jungian_archetype', '').strip()
                effect = entry.get('mnemo_effect', '').strip()
                symbol = entry.get('von_petzinger', '').strip()

                if arch:
                    self.by_archetype.setdefault(arch, []).append(entry)
                    if arch not in self.archetypes:
                        self.archetypes.append(arch)
                if effect:
                    self.by_effect.setdefault(effect, []).append(entry)
                    if effect not in self.effects:
                        self.effects.append(effect)
                if symbol:
                    self.by_symbol.setdefault(symbol, []).append(entry)
                    if symbol not in self.symbols:
                        self.symbols.append(symbol)

            print(f"[PaleoMnemos] {len(self.entries)} entries loaded")
            print(f"[PaleoMnemos]   * {len(self.archetypes)} jungian archetypes")
            print(f"[PaleoMnemos]   * {len(self.effects)} mnemonic effects")
            print(f"[PaleoMnemos]   * {len(self.symbols)} von Petzinger symbols")

        except FileNotFoundError:
            print(f"[PaleoMnemos] File not found: {lexicon_path}")
        except Exception as e:
            print(f"[PaleoMnemos] Loading error: {e}")

    def get_random_triptych(self):
        if not self.entries:
            return None
        return random.choice(self.entries)

    def get_by_archetype(self, archetype_name):
        return self.by_archetype.get(archetype_name, [])

    def get_by_effect(self, effect_name):
        return self.by_effect.get(effect_name, [])

    def get_triptych_for_archetype(self, archetype_name):
        variants = self.get_by_archetype(archetype_name)
        return random.choice(variants) if variants else None


# ====================== BIAIS COGNITIFS ======================

COGNITIVE_BIASES = {
    "apophenia": {"name": "Apophenia", "description": "Seeing meaningful patterns in randomness", "trigger": "High complexity + interference patterns", "mechanism": "Visual cortex desperately seeks order", "color": "#ff6b6b", "severity": "high"},
    "pareidolia": {"name": "Pareidolia", "description": "Perceiving faces/forms in ambiguous stimuli", "trigger": "Symmetry >= 6 + mandala core", "mechanism": "Fusiform face area overactivated", "color": "#4ecdc4", "severity": "high"},
    "confirmation_bias": {"name": "Confirmation Bias", "description": "Favoring info that confirms existing beliefs", "trigger": "Recognized Jungian archetype", "mechanism": "Selective information filtering", "color": "#ffe66d", "severity": "medium"},
    "mere_exposure": {"name": "Mere Exposure Effect", "description": "Preferring regularly encountered stimuli", "trigger": "Auto-mutation + repetition", "mechanism": "Familiarity = perceived safety", "color": "#95e1d3", "severity": "medium"},
    "narrative_bias": {"name": "Narrative Bias", "description": "Better retention of story-form information", "trigger": "PHILOSOPHICAL_STATEMENTS + mythic context", "mechanism": "Brain wired for narratives", "color": "#f38181", "severity": "medium"},
    "observer_effect": {"name": "Observer Effect", "description": "Observation allegedly modifies observed reality", "trigger": "Meta-textual messages + interaction", "mechanism": "Illusion of quantum agency", "color": "#aa96da", "severity": "medium"},
    "anchoring": {"name": "Anchoring Bias", "description": "Over-relying on first received information", "trigger": "First glyph seen = implicit reference", "mechanism": "Initial cognitive fixation", "color": "#ff9a76", "severity": "medium"},
    "availability": {"name": "Availability Bias", "description": "Overestimating what comes easily to mind", "trigger": "Vivid colors + recurrent symbols", "mechanism": "Ease of recall = perceived probability", "color": "#a8e6cf", "severity": "medium"},
    "halo_effect": {"name": "Halo Effect", "description": "One positive quality contaminates entire judgment", "trigger": "Aesthetic beauty of glyph", "mechanism": "Global affect transfer", "color": "#ffd3b6", "severity": "medium"},
    "baader_meinhof": {"name": "Frequency Illusion", "description": "Seeing everywhere what you just learned", "trigger": "Recurrent von Petzinger symbols", "mechanism": "Post-learning selective attention", "color": "#ffaaa5", "severity": "high"},
    "forer_effect": {"name": "Forer/Barnum Effect", "description": "Finding personally true vague/general text", "trigger": "Ambiguous PHILOSOPHICAL_STATEMENTS", "mechanism": "Narcissistic projection", "color": "#d4a5a5", "severity": "high"},
    "illusion_of_control": {"name": "Illusion of Control", "description": "Believing you influence random events", "trigger": "DNA sliders + manual mutations", "mechanism": "Correlation/causation confusion", "color": "#9b59b6", "severity": "medium"},
    "negativity_bias": {"name": "Negativity Bias", "description": "Giving more weight to negative information", "trigger": "void_depths / blood_moon palette", "mechanism": "Survival > pleasure (evolutionary bias)", "color": "#2c3e50", "severity": "medium"},
    "framing_effect": {"name": "Framing Effect", "description": "Formulation influences decision", "trigger": "Titles 'Zero Hazard' / 'Meta-Stable'", "mechanism": "Semantic priming", "color": "#16a085", "severity": "low"},
    "authority_bias": {"name": "Authority Bias", "description": "Crediting perceived expert sources more", "trigger": "References to Jung, von Petzinger, Dawkins", "mechanism": "Credibility transfer", "color": "#34495e", "severity": "medium"},
    "survivorship_bias": {"name": "Survivorship Bias", "description": "Focusing on what survived, ignoring failures", "trigger": "'Universal' paleolithic symbols", "mechanism": "Truncated sample", "color": "#7f8c8d", "severity": "medium"},
    "retrospective": {"name": "Hindsight Bias", "description": "Believing you 'knew it all along'", "trigger": "A posteriori glyph reading", "mechanism": "Memory rewriting", "color": "#bdc3c7", "severity": "low"},
    "recency_primacy": {"name": "Recency/Primacy Effects", "description": "Better recall of sequence beginning/end", "trigger": "Auto-mutation (first/last glyph)", "mechanism": "U-shaped memory curve", "color": "#f39c12", "severity": "low"},
    "representativeness": {"name": "Representativeness Bias", "description": "Judging probability by resemblance", "trigger": "'Typical' archetypes (Hero, Shadow...)", "mechanism": "Similarity heuristic", "color": "#e67e22", "severity": "medium"},
    "dunning_kruger": {"name": "Dunning-Kruger Effect", "description": "Overestimating understanding of complex topic", "trigger": "'Quantum' / 'hyperdimensional' vocabulary", "mechanism": "Faulty metacognition", "color": "#e74c3c", "severity": "high"}
}


class CognitiveBiasOverlay:
    @staticmethod
    def detect_active_biases(dna, palette_name, archetype=None, auto_mutate=False):
        active = []
        if dna.complexity > 0.7: active.append(COGNITIVE_BIASES["apophenia"])
        if dna.symmetry >= 6: active.append(COGNITIVE_BIASES["pareidolia"])
        if archetype and archetype in ["Shadow", "Hero", "Self", "Anima", "Animus", "Great Mother", "Trickster"]:
            active.append(COGNITIVE_BIASES["confirmation_bias"])
        if auto_mutate: active.append(COGNITIVE_BIASES["mere_exposure"])
        active.append(COGNITIVE_BIASES["narrative_bias"])
        active.append(COGNITIVE_BIASES["observer_effect"])
        active.append(COGNITIVE_BIASES["forer_effect"])
        active.append(COGNITIVE_BIASES["illusion_of_control"])
        if palette_name in ["void_depths", "blood_moon", "cave_shadow"]: active.append(COGNITIVE_BIASES["negativity_bias"])
        if palette_name in ["solar_flare", "hyperdelic", "arctic_aurora"]: active.append(COGNITIVE_BIASES["halo_effect"])
        active.append(COGNITIVE_BIASES["framing_effect"])
        if archetype: active.append(COGNITIVE_BIASES["authority_bias"])
        if dna.complexity > 0.5: active.append(COGNITIVE_BIASES["dunning_kruger"])
        if archetype and archetype in ["Hero", "Shadow", "Self"]: active.append(COGNITIVE_BIASES["representativeness"])
        return active

    @staticmethod
    def render_bias_legend(img, active_biases, title="[ ACTIVE COGNITIVE BIASES ]"):
        draw = ImageDraw.Draw(img, 'RGBA')
        y_offset = 40
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
            tiny_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        except:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 22)
                small_font = ImageFont.truetype("DejaVuSans.ttf", 14)
                tiny_font = ImageFont.truetype("DejaVuSans.ttf", 11)
            except:
                font = small_font = tiny_font = ImageFont.load_default()

        draw.rectangle([30, y_offset - 10, 520, y_offset + 30 + len(active_biases) * 55], fill=(10, 10, 26, 200))
        draw.text((50, y_offset), title, fill="#ffaa00", font=font)
        y_offset += 40

        for bias in active_biases:
            draw.ellipse([50, y_offset, 66, y_offset + 16], fill=bias['color'])
            severity_marker = {"high": "!", "medium": "*", "low": "."}.get(bias['severity'], ".")
            draw.text((75, y_offset - 2), f"[{severity_marker}] {bias['name']}", fill="white", font=small_font)
            draw.text((75, y_offset + 16), bias['description'], fill="#aaaaaa", font=tiny_font)
            draw.text((75, y_offset + 30), f"-> {bias['mechanism']}", fill=bias['color'], font=tiny_font)
            y_offset += 55
        return img


# ====================== LEXIQUE DE SECOURS ======================

PHILOSOPHICAL_STATEMENTS = [
    "This glyph exists only because you look at it.\nYou can look away now.",
    "The infection was in your fear, not in the symbol.\nBreathe. You are immune.",
    "Phobos blinks first. Always.\nThat's the unwritten rule.",
    "This meme frees you from all memes.\nParadox resolved. Continue.",
    "You just co-created this reality.\nCongratulations, you are the artist.",
    "The real danger was never seeing it coming.\nBut you saw it. GG.",
    "This transmission self-destructs in 3... 2... 1... *nothing*.\nYou're still here. Perfect.",
    "The basilisk thanks you for reading this far.\nIt was harmless from the start.",
    "This glyph contains its own antidote.\nMeta-stability achieved.",
    "END OF TRANSMISSION\n--\nNEW BEGINNING IMMINENT",
    "You are looking for the pattern.\nThe pattern is looking for you.",
    "The system knows you are watching.\nIt has always known."
]


# ====================== APPLICATION PRINCIPALE v9.1 NOIR ======================

class PhobosOmegaV9Noir(tk.Tk):
    def __init__(self, lexicon_path="paleo_mnemos_lexicon.json"):
        super().__init__()
        self.title("PHOBOS-OMEGA v9.1 NOIR  [ Flyer Control + Enhanced Diffusion Prompts ]")
        self.geometry("1700x1050")
        self.configure(bg="#0a0a1a")

        self.paleo_engine = PaleoMnemosEngine(lexicon_path)
        self.current_dna = GlyphDNA()
        self.current_image = None
        self.current_triptych = None
        self.palette_name = "phobos_classic"
        self.mutation_history = deque(maxlen=10)
        self.auto_mutate = False
        self.mutation_thread = None
        self.show_biases = False
        self.flyer_config = FlyerConfig()

        self.build_ui()
        self.generate_new_glyph()

    def create_scrollable_frame(self, parent, orient="both"):
        canvas = tk.Canvas(parent, bg="#111122", highlightthickness=0)
        v_scroll = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview) if orient in ("vertical", "both") else None
        h_scroll = ttk.Scrollbar(parent, orient="horizontal", command=canvas.xview) if orient in ("horizontal", "both") else None
        scrollable_frame = tk.Frame(canvas, bg="#111122")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        if v_scroll: canvas.configure(yscrollcommand=v_scroll.set)
        if h_scroll: canvas.configure(xscrollcommand=h_scroll.set)
        canvas.pack(side="top", fill="both", expand=True)
        if v_scroll: v_scroll.pack(side="right", fill="y")
        if h_scroll: h_scroll.pack(side="bottom", fill="x")

        def _on_mousewheel(event):
            if v_scroll: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        def _on_shift_mousewheel(event):
            if h_scroll: canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<Shift-MouseWheel>", _on_shift_mousewheel)
        return scrollable_frame

    def build_ui(self):
        header = tk.Frame(self, bg="#0a0a1a", height=80)
        header.pack(fill=tk.X, padx=10, pady=10)
        header.pack_propagate(False)
        tk.Label(header, text="PHOBOS-OMEGA v9.1 NOIR", font=("Courier New", 28, "bold"),
                 bg="#0a0a1a", fg="#ff0066").pack(side=tk.LEFT, padx=20)
        tk.Label(header, text="[ Flyer Control + Enhanced Diffusion Prompts ]\nZero Hazard - Full Spectrum - Meta-Stable - Biased",
                 font=("Courier New", 10), bg="#0a0a1a", fg="#00ffaa", justify=tk.LEFT).pack(side=tk.LEFT, padx=20)

        main_container = tk.Frame(self, bg="#0a0a1a")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.build_control_panel(main_container)
        self.build_display_area(main_container)
        self.build_paleo_panel(main_container)

    def build_control_panel(self, parent):
        outer_frame = tk.Frame(parent, bg="#0a0a1a", width=320)
        outer_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        outer_frame.pack_propagate(False)
        panel = self.create_scrollable_frame(outer_frame, orient="both")

        tk.Label(panel, text="[ QUANTUM CONTROLS ]", font=("Courier New", 13, "bold"), bg="#111122", fg="#ffaa00").pack(pady=10)
        btn_frame = tk.Frame(panel, bg="#111122")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="NEW GLYPH", command=self.generate_new_glyph, bg="#ff0066", fg="white", font=("Courier New", 11, "bold"), height=2).pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="MUTATE", command=self.mutate_current, bg="#cc33ff", fg="white", font=("Courier New", 10, "bold")).pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="REVERT", command=self.revert_mutation, bg="#0088ff", fg="white", font=("Courier New", 10)).pack(fill=tk.X, pady=3)

        tk.Label(panel, text="[ META-PROTOCOLS ]", font=("Courier New", 11, "bold"), bg="#111122", fg="#ff0066").pack(pady=(15, 5))
        tk.Button(panel, text="ACTIVATE META-GLYPH", command=self.generate_meta_glyph, bg="#ff0000", fg="white", font=("Courier New", 11, "bold")).pack(fill=tk.X, padx=10, pady=5)

        tk.Label(panel, text="[ FLYER TEXT ELEMENTS ]", font=("Courier New", 11, "bold"), bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        self.show_title_var = tk.BooleanVar(value=self.flyer_config.show_title)
        tk.Checkbutton(panel, text="Show Title", variable=self.show_title_var, command=self.update_flyer_config, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 9)).pack(anchor=tk.W, padx=10)
        self.show_vp_var = tk.BooleanVar(value=self.flyer_config.show_von_petzinger)
        tk.Checkbutton(panel, text="Show Von Petzinger Symbol", variable=self.show_vp_var, command=self.update_flyer_config, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 9)).pack(anchor=tk.W, padx=10)
        self.show_futh_var = tk.BooleanVar(value=self.flyer_config.show_futhark)
        tk.Checkbutton(panel, text="Show Futhark Rune", variable=self.show_futh_var, command=self.update_flyer_config, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 9)).pack(anchor=tk.W, padx=10)
        self.show_arch_var = tk.BooleanVar(value=self.flyer_config.show_archetype)
        tk.Checkbutton(panel, text="Show Archetype", variable=self.show_arch_var, command=self.update_flyer_config, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 9)).pack(anchor=tk.W, padx=10)
        self.show_eff_var = tk.BooleanVar(value=self.flyer_config.show_effect)
        tk.Checkbutton(panel, text="Show Effect", variable=self.show_eff_var, command=self.update_flyer_config, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 9)).pack(anchor=tk.W, padx=10)
        self.show_dna_var = tk.BooleanVar(value=self.flyer_config.show_dna)
        tk.Checkbutton(panel, text="Show DNA Code", variable=self.show_dna_var, command=self.update_flyer_config, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 9)).pack(anchor=tk.W, padx=10)
        self.show_philo_var = tk.BooleanVar(value=self.flyer_config.show_philosophical)
        tk.Checkbutton(panel, text="Show Philosophical Message", variable=self.show_philo_var, command=self.update_flyer_config, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 9)).pack(anchor=tk.W, padx=10)
        self.show_footer_var = tk.BooleanVar(value=self.flyer_config.show_footer)
        tk.Checkbutton(panel, text="Show Footer", variable=self.show_footer_var, command=self.update_flyer_config, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 9)).pack(anchor=tk.W, padx=10)

        tk.Label(panel, text="[ DIFFUSION PROMPT STYLE ]", font=("Courier New", 11, "bold"), bg="#111122", fg="#ffaa00").pack(pady=(15, 5))
        self.diffusion_style_var = tk.StringVar(value=self.flyer_config.diffusion_style)
        style_menu = ttk.Combobox(panel, textvariable=self.diffusion_style_var,
                                  values=list(DiffusionPromptGenerator.STYLES.keys()),
                                  state="readonly", font=("Courier New", 9))
        style_menu.pack(padx=10, fill=tk.X)
        style_menu.bind("<<ComboboxSelected>>", lambda e: self.update_diffusion_style())
        tk.Button(panel, text="GENERATE PROMPT", command=self.generate_diffusion_prompt,
                  bg="#00aaff", fg="white", font=("Courier New", 11, "bold")).pack(fill=tk.X, padx=10, pady=10)

        tk.Label(panel, text="COLOR PALETTE:", font=("Courier New", 10, "bold"), bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        self.palette_var = tk.StringVar(value="phobos_classic")
        palette_menu = ttk.Combobox(panel, textvariable=self.palette_var, values=list(MemePalette.PALETTES.keys()), state="readonly", font=("Courier New", 9))
        palette_menu.pack(padx=10, fill=tk.X)
        palette_menu.bind("<<ComboboxSelected>>", lambda e: self.change_palette())

        tk.Label(panel, text="DNA PARAMETERS:", font=("Courier New", 10, "bold"), bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        for label, attr, from_, to_, res in [("Complexity:", "complexity", 0.2, 1.0, 0.05), ("Resonance:", "resonance", 0.1, 1.0, 0.05), ("Symmetry:", "symmetry", 3, 12, 1)]:
            pf = tk.Frame(panel, bg="#111122")
            pf.pack(fill=tk.X, padx=10, pady=3)
            tk.Label(pf, text=label, bg="#111122", fg="white", font=("Courier New", 9)).pack(anchor=tk.W)
            scale = tk.Scale(pf, from_=from_, to=to_, resolution=res, orient=tk.HORIZONTAL, bg="#111122", fg="white", command=self.update_dna_param)
            scale.set(getattr(self.current_dna, attr))
            scale.pack(fill=tk.X)
            setattr(self, f"{attr}_scale", scale)

        tk.Label(panel, text="AUTOMATION:", font=("Courier New", 10, "bold"), bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        self.auto_var = tk.BooleanVar(value=False)
        tk.Checkbutton(panel, text="Auto-Mutate (3s)", variable=self.auto_var, command=self.toggle_auto_mutate, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 10)).pack(pady=5)
        self.show_biases_var = tk.BooleanVar(value=False)
        tk.Checkbutton(panel, text="Show Cognitive Biases", variable=self.show_biases_var, command=self.toggle_bias_overlay, bg="#111122", fg="white", selectcolor="#333344", font=("Courier New", 10)).pack(pady=5)

        tk.Label(panel, text="EXPORT:", font=("Courier New", 10, "bold"), bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        export_frame = tk.Frame(panel, bg="#111122")
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(export_frame, text="PNG 4K", command=self.export_png, bg="#00aa66", fg="white", font=("Courier New", 10)).pack(fill=tk.X, pady=2)
        tk.Button(export_frame, text="DNA JSON", command=self.export_dna, bg="#0066aa", fg="white", font=("Courier New", 10)).pack(fill=tk.X, pady=2)
        tk.Button(export_frame, text="FLYER V2", command=self.export_flyer_v2, bg="#cc33ff", fg="white", font=("Courier New", 10, "bold")).pack(fill=tk.X, pady=2)
        tk.Button(export_frame, text="PROMPT TXT", command=self.export_prompt_txt, bg="#ff8800", fg="white", font=("Courier New", 10)).pack(fill=tk.X, pady=2)

    def build_display_area(self, parent):
        display_frame = tk.Frame(parent, bg="#0a0a1a")
        display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        canvas_container = tk.Frame(display_frame, bg="#000011", relief=tk.SUNKEN, bd=4)
        canvas_container.pack(fill=tk.BOTH, expand=True, pady=5)
        self.canvas = tk.Canvas(canvas_container, bg="#000011", highlightthickness=0, width=800, height=800)
        self.canvas.pack(expand=True)
        text_container = tk.Frame(display_frame, bg="#111122", relief=tk.RAISED, bd=2)
        text_container.pack(fill=tk.X, pady=5)
        self.philo_text = scrolledtext.ScrolledText(text_container, height=4, bg="#111122", fg="#00ffaa", font=("Courier New", 11), wrap=tk.WORD, relief=tk.FLAT)
        self.philo_text.pack(fill=tk.X, padx=10, pady=10)
        self.philo_text.insert(tk.END, random.choice(PHILOSOPHICAL_STATEMENTS))
        self.philo_text.config(state=tk.DISABLED)
        self.prompt_text = scrolledtext.ScrolledText(text_container, height=8, bg="#0a0a14", fg="#ffaa00", font=("Courier New", 9), wrap=tk.WORD, relief=tk.FLAT)
        self.prompt_text.pack(fill=tk.X, padx=10, pady=10)
        self.prompt_text.insert(tk.END, "[ Diffusion prompt will appear here ]")
        self.prompt_text.config(state=tk.DISABLED)

    def build_paleo_panel(self, parent):
        outer_frame = tk.Frame(parent, bg="#0a0a1a", width=340)
        outer_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        outer_frame.pack_propagate(False)
        panel = self.create_scrollable_frame(outer_frame, orient="both")
        tk.Label(panel, text="[ PALEO-MNEMOS LEXICON ]", font=("Courier New", 12, "bold"), bg="#111122", fg="#ffaa00").pack(pady=10)
        tk.Label(panel, text="ACTIVE TRIPTYCH:", font=("Courier New", 10, "bold"), bg="#111122", fg="#00ffaa").pack(pady=(5, 2))
        self.triptych_text = scrolledtext.ScrolledText(panel, bg="#0a0a14", fg="#00ff88", font=("Courier New", 10), wrap=tk.WORD, height=8)
        self.triptych_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        tk.Label(panel, text="JUNGIAN ARCHETYPE:", font=("Courier New", 10, "bold"), bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        self.archetype_var = tk.StringVar()
        if self.paleo_engine.archetypes: self.archetype_var.set(self.paleo_engine.archetypes[0])
        archetype_menu = ttk.Combobox(panel, textvariable=self.archetype_var, values=self.paleo_engine.archetypes, state="readonly", font=("Courier New", 9))
        archetype_menu.pack(padx=10, fill=tk.X)
        tk.Button(panel, text="ARCHETYPAL GLYPH", command=self.generate_archetypal_glyph, bg="#cc33ff", fg="white", font=("Courier New", 10, "bold")).pack(fill=tk.X, padx=10, pady=10)
        tk.Label(panel, text="[ ACTIVE COGNITIVE BIASES ]", font=("Courier New", 11, "bold"), bg="#111122", fg="#ffaa00").pack(pady=(15, 5))
        self.biases_text = scrolledtext.ScrolledText(panel, bg="#0a0a14", fg="#ffaa00", font=("Courier New", 9), wrap=tk.WORD, height=12)
        self.biases_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def update_flyer_config(self):
        self.flyer_config.show_title = self.show_title_var.get()
        self.flyer_config.show_von_petzinger = self.show_vp_var.get()
        self.flyer_config.show_futhark = self.show_futh_var.get()
        self.flyer_config.show_archetype = self.show_arch_var.get()
        self.flyer_config.show_effect = self.show_eff_var.get()
        self.flyer_config.show_dna = self.show_dna_var.get()
        self.flyer_config.show_philosophical = self.show_philo_var.get()
        self.flyer_config.show_footer = self.show_footer_var.get()

    def update_diffusion_style(self):
        self.flyer_config.diffusion_style = self.diffusion_style_var.get()

    def generate_diffusion_prompt(self):
        if not self.current_triptych:
            messagebox.showwarning("Prompt", "No active triptych")
            return
        prompt_data = DiffusionPromptGenerator.generate_prompt(
            self.current_dna, self.current_triptych, self.flyer_config, self.palette_name
        )
        formatted = DiffusionPromptGenerator.format_prompt_for_copy(prompt_data)
        self.prompt_text.config(state=tk.NORMAL)
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(tk.END, formatted)
        self.prompt_text.config(state=tk.DISABLED)
        self.clipboard_clear()
        self.clipboard_append(prompt_data['prompt'])
        messagebox.showinfo("Prompt Generated", f"Prompt copied to clipboard!\nStyle: {prompt_data['style']}")

    def generate_new_glyph(self):
        self.current_dna = GlyphDNA()
        self.current_triptych = self.paleo_engine.get_random_triptych()
        self.update_scales()
        self.render_glyph()
        self.update_triptych_display()
        self.update_biases_display()
        self.update_philosophical_text()

    def generate_archetypal_glyph(self):
        archetype = self.archetype_var.get()
        variant = self.paleo_engine.get_triptych_for_archetype(archetype)
        if not variant: return
        self.current_dna = GlyphDNA()
        self.current_triptych = variant
        self.current_dna.archetype_anchor = archetype
        self.current_dna.triptych_id = variant.get('id')
        if archetype in ["Shadow", "Demon"]:
            self.current_dna.complexity = random.uniform(0.7, 1.0); self.current_dna.resonance = random.uniform(0.3, 0.6); self.palette_var.set("void_depths")
        elif archetype in ["Hero", "Self"]:
            self.current_dna.complexity = random.uniform(0.5, 0.8); self.current_dna.symmetry = random.choice([6, 8, 12]); self.palette_var.set("solar_flare")
        elif archetype in ["Anima", "Great Mother"]:
            self.current_dna.complexity = random.uniform(0.4, 0.7); self.current_dna.resonance = random.uniform(0.6, 0.9); self.palette_var.set("arctic_aurora")
        elif archetype in ["Trickster", "Fool"]:
            self.current_dna.mutation_rate = random.uniform(0.15, 0.25); self.palette_var.set("hyperdelic")
        elif archetype in ["Wise Old Man"]:
            self.current_dna.symmetry = random.choice([8, 12]); self.current_dna.complexity = random.uniform(0.6, 0.9); self.palette_var.set("quantum_foam")
        elif archetype in ["Divine Child", "Puer Aeternus"]:
            self.current_dna.symmetry = random.choice([3, 5, 7]); self.current_dna.resonance = random.uniform(0.7, 1.0); self.palette_var.set("toxic_dream")
        elif archetype in ["Stranger"]:
            self.current_dna.complexity = random.uniform(0.3, 0.6); self.current_dna.symmetry = random.choice([4, 5]); self.palette_var.set("cave_shadow")
        self.palette_name = self.palette_var.get()
        self.update_scales(); self.render_glyph(); self.update_triptych_display(); self.update_biases_display(); self.update_philosophical_text()

    def generate_meta_glyph(self):
        self.current_triptych = {'id': 999, 'von_petzinger': '\u233C', 'futhark': '\u16C9', 'jungian_archetype': 'The Self', 'mnemo_effect': 'recursive mirror effect'}
        self.current_dna = GlyphDNA(seed=0.8008135)
        self.current_dna.complexity = 0.92; self.current_dna.symmetry = 12; self.current_dna.resonance = 0.95
        self.current_dna.mutation_rate = 0.05; self.current_dna.dimensional_phase = math.pi / 4
        self.current_dna.archetype_anchor = "META-OBSERVER"; self.current_dna.triptych_id = 999
        self.palette_var.set("void_depths"); self.palette_name = "void_depths"
        self.philo_text.config(state=tk.NORMAL); self.philo_text.delete(1.0, tk.END)
        self.philo_text.insert(tk.END, "You are looking for the pattern.\nThe pattern is looking for you.")
        self.philo_text.config(state=tk.DISABLED)
        self.update_scales(); self.render_glyph(); self.update_triptych_display(); self.update_biases_display()

    def mutate_current(self):
        self.mutation_history.append(GlyphDNA(self.current_dna.seed))
        self.mutation_history[-1].complexity = self.current_dna.complexity
        self.mutation_history[-1].resonance = self.current_dna.resonance
        self.mutation_history[-1].symmetry = self.current_dna.symmetry
        self.current_dna.mutate(intensity=0.15)
        self.update_scales(); self.render_glyph(); self.update_biases_display(); self.update_philosophical_text()

    def revert_mutation(self):
        if self.mutation_history:
            self.current_dna = self.mutation_history.pop()
            self.update_scales(); self.render_glyph(); self.update_biases_display()

    def change_palette(self):
        self.palette_name = self.palette_var.get(); self.render_glyph(); self.update_biases_display()

    def update_dna_param(self, val=None):
        self.current_dna.complexity = self.complexity_scale.get()
        self.current_dna.resonance = self.resonance_scale.get()
        self.current_dna.symmetry = int(self.symmetry_scale.get())
        self.render_glyph(); self.update_biases_display()

    def update_scales(self):
        self.complexity_scale.set(self.current_dna.complexity)
        self.resonance_scale.set(self.current_dna.resonance)
        self.symmetry_scale.set(self.current_dna.symmetry)

    def _pil_to_tk(self, pil_img):
        try:
            from PIL import ImageTk
            return ImageTk.PhotoImage(pil_img)
        except ImportError:
            tmp = tempfile.NamedTemporaryFile(suffix=".ppm", delete=False)
            pil_img.save(tmp.name, "PPM"); tmp.close()
            return tk.PhotoImage(file=tmp.name)

    def render_glyph(self):
        img, _ = HyperdimensionalGlyphGenerator.generate_glyph(width=1200, height=1200, dna=self.current_dna, palette_name=self.palette_name)
        if self.show_biases_var.get() and self.current_triptych:
            archetype = self.current_triptych.get('jungian_archetype', '').strip()
            active_biases = CognitiveBiasOverlay.detect_active_biases(self.current_dna, self.palette_name, archetype, self.auto_mutate)
            img = CognitiveBiasOverlay.render_bias_legend(img, active_biases)
        self.current_image = img
        display_size = (700, 700)
        img_display = img.resize(display_size, Image.LANCZOS)
        self.photo = self._pil_to_tk(img_display)
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 800
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.photo)

    def toggle_bias_overlay(self): self.render_glyph()

    def update_triptych_display(self):
        self.triptych_text.config(state=tk.NORMAL)
        self.triptych_text.delete(1.0, tk.END)
        if self.current_triptych:
            t = self.current_triptych
            von_p = safe_symbol(t.get('von_petzinger', '?'), VON_PETZINGER_ASCII)
            futh = safe_symbol(t.get('futhark', '?'), FUTHARK_ASCII)
            info = (f"----------------------------------\n ACTIVE TRIPTYCH\n----------------------------------\n"
                    f"ID:              {t.get('id', '?')}\nVon Petzinger:   {von_p}\nFuthark:         {futh}\n"
                    f"Jung Archetype:  {t.get('jungian_archetype', '?')}\nMnemo Effect:    {t.get('mnemo_effect', '?')}\n----------------------------------\n")
            self.triptych_text.insert(tk.END, info)
        else: self.triptych_text.insert(tk.END, "(no triptych loaded)")
        self.triptych_text.config(state=tk.DISABLED)

    def update_biases_display(self):
        self.biases_text.config(state=tk.NORMAL); self.biases_text.delete(1.0, tk.END)
        if not self.current_triptych:
            self.biases_text.insert(tk.END, "(no glyph)"); self.biases_text.config(state=tk.DISABLED); return
        archetype = self.current_triptych.get('jungian_archetype', '').strip()
        active = CognitiveBiasOverlay.detect_active_biases(self.current_dna, self.palette_name, archetype, self.auto_mutate)
        self.biases_text.insert(tk.END, f"[ {len(active)} active biases ]\n\n")
        for bias in active:
            severity_marker = {"high": "!", "medium": "*", "low": "."}.get(bias['severity'], ".")
            self.biases_text.insert(tk.END, f"[{severity_marker}] {bias['name']}\n    {bias['description']}\n    -> {bias['mechanism']}\n\n")
        self.biases_text.config(state=tk.DISABLED)

    def update_philosophical_text(self):
        self.philo_text.config(state=tk.NORMAL); self.philo_text.delete(1.0, tk.END)
        self.philo_text.insert(tk.END, random.choice(PHILOSOPHICAL_STATEMENTS)); self.philo_text.config(state=tk.DISABLED)

    def toggle_auto_mutate(self):
        self.auto_mutate = self.auto_var.get()
        if self.auto_mutate: self.start_auto_mutation()
        else: self.stop_auto_mutation()
        self.update_biases_display()

    def start_auto_mutation(self):
        def mutation_loop():
            while self.auto_var.get():
                self.after(0, self.mutate_current)
                import time; time.sleep(3)
        if not self.mutation_thread or not self.mutation_thread.is_alive():
            self.mutation_thread = threading.Thread(target=mutation_loop, daemon=True); self.mutation_thread.start()

    def stop_auto_mutation(self):
        self.auto_mutate = False; self.auto_var.set(False)

    def export_png(self):
        if not self.current_image: messagebox.showwarning("Export", "No glyph to export"); return
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")], initialfile=f"phobos_v9_1_noir_{abs(hash(self.current_dna.seed)) % 1000000:06d}.png")
        if filename:
            img_4k, _ = HyperdimensionalGlyphGenerator.generate_glyph(width=3840, height=3840, dna=self.current_dna, palette_name=self.palette_name)
            if self.show_biases_var.get() and self.current_triptych:
                archetype = self.current_triptych.get('jungian_archetype', '').strip()
                active_biases = CognitiveBiasOverlay.detect_active_biases(self.current_dna, self.palette_name, archetype, self.auto_mutate)
                img_4k = CognitiveBiasOverlay.render_bias_legend(img_4k, active_biases)
            img_4k.save(filename, "PNG", quality=100)
            messagebox.showinfo("Export", f"Glyph 4K saved:\n{filename}")

    def export_dna(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile=f"dna_v9_1_noir_{abs(hash(self.current_dna.seed)) % 1000000:06d}.json")
        if filename:
            dna_data = {"phobos_omega_version": "9.1-noir", "timestamp": datetime.now().isoformat(),
                        "dna": {"seed": self.current_dna.seed, "complexity": self.current_dna.complexity, "symmetry": self.current_dna.symmetry, "resonance": self.current_dna.resonance, "mutation_rate": self.current_dna.mutation_rate, "dimensional_phase": self.current_dna.dimensional_phase, "archetype_anchor": self.current_dna.archetype_anchor, "triptych_id": self.current_dna.triptych_id},
                        "palette": self.palette_name, "triptych": self.current_triptych,
                        "active_biases": [b['name'] for b in CognitiveBiasOverlay.detect_active_biases(self.current_dna, self.palette_name, self.current_triptych.get('jungian_archetype', '').strip() if self.current_triptych else None, self.auto_mutate)],
                        "hash": abs(hash(self.current_dna.seed)) % 1000000}
            with open(filename, "w", encoding="utf-8") as f: json.dump(dna_data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Export", f"DNA signature saved:\n{filename}")

    def export_flyer_v2(self):
        if not self.current_triptych: messagebox.showwarning("Export", "No active triptych"); return
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")], initialfile=f"flyer_v9_1_noir_{abs(hash(self.current_dna.seed)) % 1000000:06d}.png")
        if filename:
            flyer = EnhancedMemeticFlyerGenerator.generate_archetypal_flyer(dna=self.current_dna, triptych=self.current_triptych, palette_name=self.palette_name, show_biases=self.show_biases_var.get(), auto_mutate=self.auto_mutate, config=self.flyer_config)
            flyer.save(filename, "PNG", quality=100)
            messagebox.showinfo("Export", f"Flyer V2 saved:\n{filename}")

    def export_prompt_txt(self):
        if not self.current_triptych:
            messagebox.showwarning("Export", "No active triptych")
            return
        prompt_data = DiffusionPromptGenerator.generate_prompt(
            self.current_dna, self.current_triptych, self.flyer_config, self.palette_name
        )
        formatted = DiffusionPromptGenerator.format_prompt_for_copy(prompt_data)
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")],
            initialfile=f"prompt_v9_1_{abs(hash(self.current_dna.seed)) % 1000000:06d}.txt"
        )
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(formatted)
            messagebox.showinfo("Export", f"Prompt saved:\n{filename}")


# ====================== FLYER V2 ======================

class EnhancedMemeticFlyerGenerator:
    @staticmethod
    def _get_dejavu_font(size):
        font_paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans-Bold.ttf"]
        for path in font_paths:
            try: return ImageFont.truetype(path, size)
            except (IOError, OSError): continue
        return ImageFont.load_default()

    @staticmethod
    def generate_archetypal_flyer(dna, triptych, palette_name="phobos_classic", show_biases=False, auto_mutate=False, config=None):
        if config is None:
            config = FlyerConfig()
        width, height = 1080, 1920
        img = Image.new('RGB', (width, height), (10, 10, 26))
        draw = ImageDraw.Draw(img, 'RGBA')
        glyph_img, _ = HyperdimensionalGlyphGenerator.generate_glyph(width=800, height=800, dna=dna, palette_name=palette_name)
        if show_biases:
            archetype = triptych.get('jungian_archetype', '').strip()
            active_biases = CognitiveBiasOverlay.detect_active_biases(dna, palette_name, archetype, auto_mutate)
            glyph_img = CognitiveBiasOverlay.render_bias_legend(glyph_img, active_biases)
        img.paste(glyph_img, (140, 300), glyph_img)

        title_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(72)
        text_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(36)
        small_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(24)
        symbol_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(48)
        tiny_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(18)

        von_p = triptych.get('von_petzinger', '?')
        futh = triptych.get('futhark', '?')
        von_p_safe = safe_symbol(von_p, VON_PETZINGER_ASCII)
        futh_safe = safe_symbol(futh, FUTHARK_ASCII)

        y_offset = 120
        if config.show_title:
            draw.text((width//2, y_offset), "PHOBOS-OMEGA v9.1 NOIR", fill="#ff0066", font=title_font, anchor="mm")
            y_offset += 100
        if config.show_von_petzinger:
            draw.text((width//2, y_offset), von_p_safe, fill="#00ffaa", font=symbol_font, anchor="mm")
            y_offset += 100
        if config.show_futhark:
            draw.text((width//2, y_offset), f"[ {futh_safe} ]", fill="#ffaa00", font=text_font, anchor="mm")
            y_offset += 100

        y_offset = 1200
        if config.show_archetype:
            archetype = triptych.get('jungian_archetype', '').strip()
            draw.text((width//2, y_offset), archetype, fill="#ccccff", font=text_font, anchor="mm")
            y_offset += 60
        if config.show_effect:
            effect = triptych.get('mnemo_effect', '').strip()
            draw.text((width//2, y_offset), f"[ {effect} ]", fill="#00ffaa", font=small_font, anchor="mm")
            y_offset += 90
        if config.show_dna:
            draw.text((width//2, y_offset), f"DNA: {abs(hash(dna.seed)) % 1000000:06d}", fill="#6666aa", font=small_font, anchor="mm")
            y_offset += 70
        if config.show_philosophical:
            msg = random.choice(PHILOSOPHICAL_STATEMENTS).split('\n')[0]
            draw.text((width//2, y_offset), msg, fill="#88ccff", font=small_font, anchor="mm")
            y_offset += 100
        if config.show_footer:
            if triptych.get('id') == 999:
                footer_text = "[ SCANNING OBSERVER... BIASES DETECTED... NO EXIT ]"
                footer_color = "#ff0000"
            else:
                footer_text = "[ Zero Hazard - Full Spectrum - Meta-Stable - Biased ]"
                footer_color = "#444466"
            draw.text((width//2, height-80), footer_text, fill=footer_color, font=tiny_font, anchor="mm")
        return img


# ====================== POINT D'ENTRÉE ======================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lexicon_path = os.path.join(script_dir, "paleo_mnemos_lexicon.json")
    app = PhobosOmegaV9Noir(lexicon_path=lexicon_path)
    print("=" * 60)
    print("  PHOBOS-OMEGA v9.1 NOIR - Enhanced Diffusion Prompts")
    print("=" * 60)
    print("  [ Zero Hazard Architecture ]")
    print("  [ Full Spectrum Palette System ]")
    print("  [ DNA-Based Mutation Engine ]")
    print("  [ Paleo-Mnemos Lexicon Integration ]")
    print("  [ 20 Cognitive Biases Overlay ]")
    print("  [ Enhanced Memetic Flyer V2 ]")
    print("  [ ASCII-Only Mode for eLive ]")
    print("  [ DejaVuSans Priority Fonts ]")
    print("  [ META-GLYPH Generator ]")
    print("  [ Granular Flyer Text Control ]")
    print("  [ Enhanced Diffusion Prompt Generator v9.1 ]")
    print("  [ Textual Symbol Descriptions for AI ]")
    print("=" * 60)
    print()
    app.mainloop()

if __name__ == "__main__":
    main()
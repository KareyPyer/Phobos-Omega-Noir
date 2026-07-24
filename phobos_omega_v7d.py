#!/usr/bin/env python3
# PHOBOS-Ω v7d - Paleo-Mnemos Memetic Engine
# VERSION OPTIMISÉE POUR eLive / distributions minimalistes
# - DejaVuSans prioritaire (confirmé présent)
# - Fallbacks ASCII complets
# - Bug Tkinter stop_auto_mutation corrigé
# - Fallback PPM si ImageTk indisponible

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random, os, json, math, tempfile
from datetime import datetime
from collections import deque
import threading

# ====================== CONSTANTES & FALLBACKS ASCII ======================

# Mapping Unicode -> ASCII pour TOUS les textes
UNICODE_TO_ASCII = {
    'Ω': 'OMEGA',
    '⟡': '[*]',
    '•': '-',
    'É': 'E',
    'è': 'e',
    'ê': 'e',
    'É': 'E',
    'à': 'a',
    'ù': 'u',
    'ç': 'c',
    'ô': 'o',
    'î': 'i',
    'û': 'u',
    'â': 'a',
    'ë': 'e',
    'ï': 'i',
    'ü': 'u',
    'ö': 'o',
    'ä': 'a',
    '—': '--',
    '…': '...',
    '⚠': '!',
    '◆': '*',
    '◇': '.',
    '→': '->',
    '█': '#',
    '━': '-',
}

# Fallbacks pour les symboles spéciaux
VON_PETZINGER_ASCII = {
    "△": "[TRI]", "▫": "[SQR]", "⧆": "[CUBE]", "⧈": "[BOX]",
    "⨀": "[CIR]", "⛶": "[FRAME]", "⬠": "[PENT]", "⬡": "[HEX]",
    "⬢": "[HEX2]", "⯁": "[SEPT]", "": "[ARROW]", "⧉": "[DBOX]",
    "⦻": "[CROSS]", "⌾": "[RING]", "⌽": "[HALF]", "⌼": "[GRID]",
    "⌺": "[MESH]", "⌻": "[NET]", "⌰": "[PIPE]", "⨯": "[X]",
    "⧖": "[HOUR]", "⧗": "[TIME]", "": "[FLOW]", "⧙": "[WAVE]",
    "⧚": "[SPIRAL]", "⧛": "[VORTEX]"
}

FUTHARK_ASCII = {
    "ᚠ": "F", "ᚢ": "U", "ᚦ": "TH", "ᚨ": "A", "ᚱ": "R",
    "ᚲ": "K", "ᚷ": "G", "": "W", "ᚺ": "H", "ᚾ": "N",
    "ᛁ": "I", "ᛃ": "J", "ᛇ": "EO", "ᛈ": "P", "ᛉ": "Z",
    "ᛋ": "S", "ᛏ": "T", "": "B", "ᛖ": "E", "ᛗ": "M",
    "ᛚ": "L", "ᛜ": "NG", "ᛟ": "O", "ᛞ": "D", "ᚣ": "YR",
    "ᛡ": "IA", "ᛠ": "EA"
}


def to_ascii(text):
    """Convertit un texte Unicode en ASCII-safe"""
    if not text:
        return ""
    result = text
    for unicode_char, ascii_char in UNICODE_TO_ASCII.items():
        result = result.replace(unicode_char, ascii_char)
    return result


def safe_symbol(symbol, fallback_dict):
    """Retourne le fallback ASCII si le symbole n'est pas ASCII"""
    if not symbol:
        return "?"
    # Si le symbole contient des caractères non-ASCII
    if any(ord(c) > 127 for c in symbol):
        return fallback_dict.get(symbol, symbol)
    return symbol


# ====================== ARCHITECTURE NEURALE ======================

class MemePalette:
    """Palettes chromatiques psycho-actives"""
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
    """ADN génératif pour mutations cohérentes"""
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
    """Générateur de glyphes avec géométrie non-euclidienne"""

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
        """Motif d'interférence ondulatoire"""
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
            # CORRECTION : utiliser draw.line au lieu de draw.polygon
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
    """Moteur d'indexation du lexique Paleo-Mnemos"""

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

            print(f"[PaleoMnemos] ✓ {len(self.entries)} entrées chargées")
            print(f"[PaleoMnemos]   • {len(self.archetypes)} archétypes jungiens")
            print(f"[PaleoMnemos]   • {len(self.effects)} effets mnésiques")
            print(f"[PaleoMnemos]   • {len(self.symbols)} symboles von Petzinger")

        except FileNotFoundError:
            print(f"[PaleoMnemos] ✗ Fichier introuvable: {lexicon_path}")
        except Exception as e:
            print(f"[PaleoMnemos] ✗ Erreur de chargement: {e}")

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
    "apophenia": {
        "name": "Apophenia",
        "description": "Seeing meaningful patterns in randomness",
        "trigger": "High complexity + interference patterns",
        "mechanism": "Visual cortex desperately seeks order",
        "color": "#ff6b6b",
        "severity": "high"
    },
    "pareidolia": {
        "name": "Pareidolia",
        "description": "Perceiving faces/forms in ambiguous stimuli",
        "trigger": "Symmetry >= 6 + mandala core",
        "mechanism": "Fusiform face area overactivated",
        "color": "#4ecdc4",
        "severity": "high"
    },
    "confirmation_bias": {
        "name": "Confirmation Bias",
        "description": "Favoring info that confirms existing beliefs",
        "trigger": "Recognized Jungian archetype",
        "mechanism": "Selective information filtering",
        "color": "#ffe66d",
        "severity": "medium"
    },
    "mere_exposure": {
        "name": "Mere Exposure Effect",
        "description": "Preferring regularly encountered stimuli",
        "trigger": "Auto-mutation + repetition",
        "mechanism": "Familiarity = perceived safety",
        "color": "#95e1d3",
        "severity": "medium"
    },
    "narrative_bias": {
        "name": "Narrative Bias",
        "description": "Better retention of story-form information",
        "trigger": "PHILOSOPHICAL_STATEMENTS + mythic context",
        "mechanism": "Brain wired for narratives",
        "color": "#f38181",
        "severity": "medium"
    },
    "observer_effect": {
        "name": "Observer Effect",
        "description": "Observation allegedly modifies observed reality",
        "trigger": "Meta-textual messages + interaction",
        "mechanism": "Illusion of quantum agency",
        "color": "#aa96da",
        "severity": "medium"
    },
    "anchoring": {
        "name": "Anchoring Bias",
        "description": "Over-relying on first received information",
        "trigger": "First glyph seen = implicit reference",
        "mechanism": "Initial cognitive fixation",
        "color": "#ff9a76",
        "severity": "medium"
    },
    "availability": {
        "name": "Availability Bias",
        "description": "Overestimating what comes easily to mind",
        "trigger": "Vivid colors + recurrent symbols",
        "mechanism": "Ease of recall = perceived probability",
        "color": "#a8e6cf",
        "severity": "medium"
    },
    "halo_effect": {
        "name": "Halo Effect",
        "description": "One positive quality contaminates entire judgment",
        "trigger": "Aesthetic beauty of glyph",
        "mechanism": "Global affect transfer",
        "color": "#ffd3b6",
        "severity": "medium"
    },
    "baader_meinhof": {
        "name": "Frequency Illusion",
        "description": "Seeing everywhere what you just learned",
        "trigger": "Recurrent von Petzinger symbols",
        "mechanism": "Post-learning selective attention",
        "color": "#ffaaa5",
        "severity": "high"
    },
    "forer_effect": {
        "name": "Forer/Barnum Effect",
        "description": "Finding personally true vague/general text",
        "trigger": "Ambiguous PHILOSOPHICAL_STATEMENTS",
        "mechanism": "Narcissistic projection",
        "color": "#d4a5a5",
        "severity": "high"
    },
    "illusion_of_control": {
        "name": "Illusion of Control",
        "description": "Believing you influence random events",
        "trigger": "DNA sliders + manual mutations",
        "mechanism": "Correlation/causation confusion",
        "color": "#9b59b6",
        "severity": "medium"
    },
    "negativity_bias": {
        "name": "Negativity Bias",
        "description": "Giving more weight to negative information",
        "trigger": "void_depths / blood_moon palette",
        "mechanism": "Survival > pleasure (evolutionary bias)",
        "color": "#2c3e50",
        "severity": "medium"
    },
    "framing_effect": {
        "name": "Framing Effect",
        "description": "Formulation influences decision",
        "trigger": "Titles 'Zero Hazard' / 'Meta-Stable'",
        "mechanism": "Semantic priming",
        "color": "#16a085",
        "severity": "low"
    },
    "authority_bias": {
        "name": "Authority Bias",
        "description": "Crediting perceived expert sources more",
        "trigger": "References to Jung, von Petzinger, Dawkins",
        "mechanism": "Credibility transfer",
        "color": "#34495e",
        "severity": "medium"
    },
    "survivorship_bias": {
        "name": "Survivorship Bias",
        "description": "Focusing on what survived, ignoring failures",
        "trigger": "'Universal' paleolithic symbols",
        "mechanism": "Truncated sample",
        "color": "#7f8c8d",
        "severity": "medium"
    },
    "retrospective": {
        "name": "Hindsight Bias",
        "description": "Believing you 'knew it all along'",
        "trigger": "A posteriori glyph reading",
        "mechanism": "Memory rewriting",
        "color": "#bdc3c7",
        "severity": "low"
    },
    "recency_primacy": {
        "name": "Recency/Primacy Effects",
        "description": "Better recall of sequence beginning/end",
        "trigger": "Auto-mutation (first/last glyph)",
        "mechanism": "U-shaped memory curve",
        "color": "#f39c12",
        "severity": "low"
    },
    "representativeness": {
        "name": "Representativeness Bias",
        "description": "Judging probability by resemblance",
        "trigger": "'Typical' archetypes (Hero, Shadow...)",
        "mechanism": "Similarity heuristic",
        "color": "#e67e22",
        "severity": "medium"
    },
    "dunning_kruger": {
        "name": "Dunning-Kruger Effect",
        "description": "Overestimating understanding of complex topic",
        "trigger": "'Quantum' / 'hyperdimensional' vocabulary",
        "mechanism": "Faulty metacognition",
        "color": "#e74c3c",
        "severity": "high"
    }
}


class CognitiveBiasOverlay:
    """Overlay visuel montrant quels biais sont activés par un glyphe"""

    @staticmethod
    def detect_active_biases(dna, palette_name, archetype=None, auto_mutate=False):
        active = []

        if dna.complexity > 0.7:
            active.append(COGNITIVE_BIASES["apophenia"])
        if dna.symmetry >= 6:
            active.append(COGNITIVE_BIASES["pareidolia"])
        if archetype and archetype in ["L'Ombre", "Le Héros", "Le Self", "L'Anima", "L'Animus",
                                       "La Grande Mère", "Le Trickster"]:
            active.append(COGNITIVE_BIASES["confirmation_bias"])
        if auto_mutate:
            active.append(COGNITIVE_BIASES["mere_exposure"])
        active.append(COGNITIVE_BIASES["narrative_bias"])
        active.append(COGNITIVE_BIASES["observer_effect"])
        active.append(COGNITIVE_BIASES["forer_effect"])
        active.append(COGNITIVE_BIASES["illusion_of_control"])
        if palette_name in ["void_depths", "blood_moon", "cave_shadow"]:
            active.append(COGNITIVE_BIASES["negativity_bias"])
        if palette_name in ["solar_flare", "hyperdelic", "arctic_aurora"]:
            active.append(COGNITIVE_BIASES["halo_effect"])
        active.append(COGNITIVE_BIASES["framing_effect"])
        if archetype:
            active.append(COGNITIVE_BIASES["authority_bias"])
        if dna.complexity > 0.5:
            active.append(COGNITIVE_BIASES["dunning_kruger"])
        if archetype and archetype in ["Le Héros", "L'Ombre", "Le Self"]:
            active.append(COGNITIVE_BIASES["representativeness"])

        return active

    @staticmethod
    def render_bias_legend(img, active_biases, title="[ ACTIVE COGNITIVE BIASES ]"):
        """v7d : Overlay avec polices DejaVuSans et marqueurs ASCII"""
        draw = ImageDraw.Draw(img, 'RGBA')
        y_offset = 40

        # v7d : polices DejaVuSans (chemins Debian/Ubuntu)
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

        # Fond semi-transparent
        draw.rectangle([30, y_offset - 10, 520, y_offset + 30 + len(active_biases) * 55],
                       fill=(10, 10, 26, 200))

        draw.text((50, y_offset), title, fill="#ffaa00", font=font)
        y_offset += 40

        for bias in active_biases:
            # Cercle coloré
            draw.ellipse([50, y_offset, 66, y_offset + 16], fill=bias['color'])

            # v7d : Marqueurs ASCII-safe
            severity_marker = {"high": "!", "medium": "*", "low": "."}.get(bias['severity'], ".")
            draw.text((75, y_offset - 2), f"[{severity_marker}] {bias['name']}",
                      fill="white", font=small_font)

            draw.text((75, y_offset + 16), bias['description'],
                      fill="#aaaaaa", font=tiny_font)
            draw.text((75, y_offset + 30), f"-> {bias['mechanism']}",
                      fill=bias['color'], font=tiny_font)

            y_offset += 55

        return img


# ====================== LEXIQUE DE SECOURS ======================

QUANTUM_LEXICON = {
    "archetypes": [
        "The Quantum Observer", "The Incarnate Paradox", "The Living Entropy",
        "The Bifurcation Guardian", "The Void Architect", "The Probability Weaver",
        "The Fractal Consciousness", "The Wave Decoder", "The Primordial Echo"
    ],
    "effects": [
        "hyperdimensional resonance", "controlled probabilistic collapse",
        "amplified synchronicity", "temporal derivation", "memetic fusion",
        "dormant node activation", "chaotic harmonization"
    ],
    "symbols": ["[TRI]", "[SQR]", "[CUBE]", "[BOX]", "[CIR]", "[FRAME]"],
    "runes": ["F", "U", "TH", "A", "R", "K", "G", "W", "H", "N", "I", "J"]
}

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
    "END OF TRANSMISSION\n--\nNEW BEGINNING IMMINENT"
]


# ====================== APPLICATION PRINCIPALE v7d ======================

class PhobosOmegaV7d(tk.Tk):
    def __init__(self, lexicon_path="paleo_mnemos_lexicon.json"):
        super().__init__()
        self.title("PHOBOS-OMEGA v7d  [ Paleo-Mnemos Memetic Engine ]")
        self.geometry("1700x1050")
        self.configure(bg="#0a0a1a")

        self.paleo_engine = PaleoMnemosEngine(lexicon_path)

        self.current_dna = GlyphDNA()
        self.current_image = None
        self.current_triptych = None
        self.palette_name = "phobos_classic"
        self.mutation_history = deque(maxlen=10)
        self.auto_mutate = False  # v7d : variable explicite
        self.mutation_thread = None
        self.show_biases = False

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
        # Header
        header = tk.Frame(self, bg="#0a0a1a", height=80)
        header.pack(fill=tk.X, padx=10, pady=10)
        header.pack_propagate(False)
        tk.Label(header, text="PHOBOS-OMEGA v7d", font=("Courier New", 32, "bold"),
                 bg="#0a0a1a", fg="#ff0066").pack(side=tk.LEFT, padx=20)
        # v7d : ASCII-safe pour Tkinter
        tk.Label(header, text="[ Paleo-Mnemos Memetic Engine ]\nZero Hazard - Full Spectrum - Meta-Stable - Biased",
                 font=("Courier New", 11), bg="#0a0a1a", fg="#00ffaa",
                 justify=tk.LEFT).pack(side=tk.LEFT, padx=20)

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

        tk.Label(panel, text="[ QUANTUM CONTROLS ]", font=("Courier New", 13, "bold"),
                 bg="#111122", fg="#ffaa00").pack(pady=10)

        btn_frame = tk.Frame(panel, bg="#111122")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="NEW GLYPH", command=self.generate_new_glyph,
                  bg="#ff0066", fg="white", font=("Courier New", 11, "bold"), height=2
                  ).pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="MUTATE", command=self.mutate_current,
                  bg="#cc33ff", fg="white", font=("Courier New", 10, "bold")
                  ).pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="REVERT", command=self.revert_mutation,
                  bg="#0088ff", fg="white", font=("Courier New", 10)
                  ).pack(fill=tk.X, pady=3)

        tk.Label(panel, text="COLOR PALETTE:", font=("Courier New", 10, "bold"),
                 bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        self.palette_var = tk.StringVar(value="phobos_classic")
        palette_menu = ttk.Combobox(panel, textvariable=self.palette_var,
                                    values=list(MemePalette.PALETTES.keys()),
                                    state="readonly", font=("Courier New", 9))
        palette_menu.pack(padx=10, fill=tk.X)
        palette_menu.bind("<<ComboboxSelected>>", lambda e: self.change_palette())

        tk.Label(panel, text="DNA PARAMETERS:", font=("Courier New", 10, "bold"),
                 bg="#111122", fg="#00ffaa").pack(pady=(15, 5))

        for label, attr, from_, to_, res in [
            ("Complexity:", "complexity", 0.2, 1.0, 0.05),
            ("Resonance:", "resonance", 0.1, 1.0, 0.05),
            ("Symmetry:", "symmetry", 3, 12, 1)
        ]:
            pf = tk.Frame(panel, bg="#111122")
            pf.pack(fill=tk.X, padx=10, pady=3)
            tk.Label(pf, text=label, bg="#111122", fg="white", font=("Courier New", 9)).pack(anchor=tk.W)
            scale = tk.Scale(pf, from_=from_, to=to_, resolution=res, orient=tk.HORIZONTAL,
                             bg="#111122", fg="white", command=self.update_dna_param)
            scale.set(getattr(self.current_dna, attr))
            scale.pack(fill=tk.X)
            setattr(self, f"{attr}_scale", scale)

        tk.Label(panel, text="AUTOMATION:", font=("Courier New", 10, "bold"),
                 bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        self.auto_var = tk.BooleanVar(value=False)
        tk.Checkbutton(panel, text="Auto-Mutate (3s)", variable=self.auto_var,
                       command=self.toggle_auto_mutate, bg="#111122", fg="white",
                       selectcolor="#333344", font=("Courier New", 10)).pack(pady=5)

        self.show_biases_var = tk.BooleanVar(value=False)
        tk.Checkbutton(panel, text="Show Cognitive Biases",
                       variable=self.show_biases_var, command=self.toggle_bias_overlay,
                       bg="#111122", fg="white", selectcolor="#333344",
                       font=("Courier New", 10)).pack(pady=5)

        tk.Label(panel, text="EXPORT:", font=("Courier New", 10, "bold"),
                 bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        export_frame = tk.Frame(panel, bg="#111122")
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(export_frame, text="PNG 4K", command=self.export_png,
                  bg="#00aa66", fg="white", font=("Courier New", 10)).pack(fill=tk.X, pady=2)
        tk.Button(export_frame, text="DNA JSON", command=self.export_dna,
                  bg="#0066aa", fg="white", font=("Courier New", 10)).pack(fill=tk.X, pady=2)
        tk.Button(export_frame, text="FLYER V2", command=self.export_flyer_v2,
                  bg="#cc33ff", fg="white", font=("Courier New", 10, "bold")).pack(fill=tk.X, pady=2)

    def build_display_area(self, parent):
        display_frame = tk.Frame(parent, bg="#0a0a1a")
        display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        canvas_container = tk.Frame(display_frame, bg="#000011", relief=tk.SUNKEN, bd=4)
        canvas_container.pack(fill=tk.BOTH, expand=True, pady=5)
        self.canvas = tk.Canvas(canvas_container, bg="#000011", highlightthickness=0,
                                width=800, height=800)
        self.canvas.pack(expand=True)

        text_container = tk.Frame(display_frame, bg="#111122", relief=tk.RAISED, bd=2)
        text_container.pack(fill=tk.X, pady=5)
        self.philo_text = scrolledtext.ScrolledText(text_container, height=4, bg="#111122",
                                                    fg="#00ffaa", font=("Courier New", 11),
                                                    wrap=tk.WORD, relief=tk.FLAT)
        self.philo_text.pack(fill=tk.X, padx=10, pady=10)
        self.philo_text.insert(tk.END, random.choice(PHILOSOPHICAL_STATEMENTS))
        self.philo_text.config(state=tk.DISABLED)

    def build_paleo_panel(self, parent):
        outer_frame = tk.Frame(parent, bg="#0a0a1a", width=340)
        outer_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        outer_frame.pack_propagate(False)
        panel = self.create_scrollable_frame(outer_frame, orient="both")

        tk.Label(panel, text="[ PALEO-MNEMOS LEXICON ]", font=("Courier New", 12, "bold"),
                 bg="#111122", fg="#ffaa00").pack(pady=10)

        tk.Label(panel, text="ACTIVE TRIPTYCH:", font=("Courier New", 10, "bold"),
                 bg="#111122", fg="#00ffaa").pack(pady=(5, 2))
        self.triptych_text = scrolledtext.ScrolledText(panel, bg="#0a0a14", fg="#00ff88",
                                                       font=("Courier New", 10),
                                                       wrap=tk.WORD, height=8)
        self.triptych_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(panel, text="JUNGIAN ARCHETYPE:", font=("Courier New", 10, "bold"),
                 bg="#111122", fg="#00ffaa").pack(pady=(15, 5))
        self.archetype_var = tk.StringVar()
        if self.paleo_engine.archetypes:
            self.archetype_var.set(self.paleo_engine.archetypes[0])
        archetype_menu = ttk.Combobox(panel, textvariable=self.archetype_var,
                                      values=self.paleo_engine.archetypes,
                                      state="readonly", font=("Courier New", 9))
        archetype_menu.pack(padx=10, fill=tk.X)

        tk.Button(panel, text="ARCHETYPAL GLYPH",
                  command=self.generate_archetypal_glyph,
                  bg="#cc33ff", fg="white", font=("Courier New", 10, "bold")
                  ).pack(fill=tk.X, padx=10, pady=10)

        tk.Label(panel, text="[ ACTIVE COGNITIVE BIASES ]", font=("Courier New", 11, "bold"),
                 bg="#111122", fg="#ffaa00").pack(pady=(15, 5))
        self.biases_text = scrolledtext.ScrolledText(panel, bg="#0a0a14", fg="#ffaa00",
                                                     font=("Courier New", 9),
                                                     wrap=tk.WORD, height=12)
        self.biases_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # ===== Actions =====

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
        if not variant:
            return

        self.current_dna = GlyphDNA()
        self.current_triptych = variant
        self.current_dna.archetype_anchor = archetype
        self.current_dna.triptych_id = variant.get('id')

        if archetype in ["L'Ombre", "Le Démon"]:
            self.current_dna.complexity = random.uniform(0.7, 1.0)
            self.current_dna.resonance = random.uniform(0.3, 0.6)
            self.palette_var.set("void_depths")
        elif archetype in ["Le Héros", "Le Self"]:
            self.current_dna.complexity = random.uniform(0.5, 0.8)
            self.current_dna.symmetry = random.choice([6, 8, 12])
            self.palette_var.set("solar_flare")
        elif archetype in ["L'Anima", "La Grande Mère"]:
            self.current_dna.complexity = random.uniform(0.4, 0.7)
            self.current_dna.resonance = random.uniform(0.6, 0.9)
            self.palette_var.set("arctic_aurora")
        elif archetype in ["Le Trickster", "Le Sage Fou"]:
            self.current_dna.mutation_rate = random.uniform(0.15, 0.25)
            self.palette_var.set("hyperdelic")
        elif archetype in ["Le Vieillard Sage"]:
            self.current_dna.symmetry = random.choice([8, 12])
            self.current_dna.complexity = random.uniform(0.6, 0.9)
            self.palette_var.set("quantum_foam")
        elif archetype in ["L'Enfant Divin", "Le Puer Aeternus"]:
            self.current_dna.symmetry = random.choice([3, 5, 7])
            self.current_dna.resonance = random.uniform(0.7, 1.0)
            self.palette_var.set("toxic_dream")
        elif archetype in ["L'Étranger"]:
            self.current_dna.complexity = random.uniform(0.3, 0.6)
            self.current_dna.symmetry = random.choice([4, 5])
            self.palette_var.set("cave_shadow")

        self.palette_name = self.palette_var.get()
        self.update_scales()
        self.render_glyph()
        self.update_triptych_display()
        self.update_biases_display()
        self.update_philosophical_text()

    def mutate_current(self):
        self.mutation_history.append(GlyphDNA(self.current_dna.seed))
        self.mutation_history[-1].complexity = self.current_dna.complexity
        self.mutation_history[-1].resonance = self.current_dna.resonance
        self.mutation_history[-1].symmetry = self.current_dna.symmetry
        self.current_dna.mutate(intensity=0.15)
        self.update_scales()
        self.render_glyph()
        self.update_biases_display()
        self.update_philosophical_text()

    def revert_mutation(self):
        if self.mutation_history:
            self.current_dna = self.mutation_history.pop()
            self.update_scales()
            self.render_glyph()
            self.update_biases_display()

    def change_palette(self):
        self.palette_name = self.palette_var.get()
        self.render_glyph()
        self.update_biases_display()

    def update_dna_param(self, val=None):
        self.current_dna.complexity = self.complexity_scale.get()
        self.current_dna.resonance = self.resonance_scale.get()
        self.current_dna.symmetry = int(self.symmetry_scale.get())
        self.render_glyph()
        self.update_biases_display()

    def update_scales(self):
        self.complexity_scale.set(self.current_dna.complexity)
        self.resonance_scale.set(self.current_dna.resonance)
        self.symmetry_scale.set(self.current_dna.symmetry)

    def _pil_to_tk(self, pil_img):
        """v7d : Conversion PIL -> Tkinter avec fallback PPM"""
        try:
            from PIL import ImageTk
            return ImageTk.PhotoImage(pil_img)
        except ImportError:
            # Fallback PPM (nécessite juste Tkinter)
            tmp = tempfile.NamedTemporaryFile(suffix=".ppm", delete=False)
            pil_img.save(tmp.name, "PPM")
            tmp.close()
            return tk.PhotoImage(file=tmp.name)

    def render_glyph(self):
        img, _ = HyperdimensionalGlyphGenerator.generate_glyph(
            width=1200, height=1200, dna=self.current_dna, palette_name=self.palette_name
        )

        if self.show_biases_var.get() and self.current_triptych:
            archetype = self.current_triptych.get('jungian_archetype', '').strip()
            active_biases = CognitiveBiasOverlay.detect_active_biases(
                self.current_dna, self.palette_name, archetype, self.auto_mutate
            )
            img = CognitiveBiasOverlay.render_bias_legend(img, active_biases)

        self.current_image = img
        display_size = (700, 700)
        img_display = img.resize(display_size, Image.LANCZOS)

        # v7d : conversion avec fallback
        self.photo = self._pil_to_tk(img_display)

        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 800
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.photo)

    def toggle_bias_overlay(self):
        self.render_glyph()

    def update_triptych_display(self):
        self.triptych_text.config(state=tk.NORMAL)
        self.triptych_text.delete(1.0, tk.END)
        if self.current_triptych:
            t = self.current_triptych
            # ✅ v7d : CORRECTION - appel de la bonne fonction safe_symbol
            von_p = safe_symbol(t.get('von_petzinger', '?'), VON_PETZINGER_ASCII)
            futh = safe_symbol(t.get('futhark', '?'), FUTHARK_ASCII)
            
            info = (
                "----------------------------------\n"
                " ACTIVE TRIPTYCH\n"
                "----------------------------------\n"
                f"ID:              {t.get('id', '?')}\n"
                f"Von Petzinger:   {von_p}\n"
                f"Futhark:         {futh}\n"
                f"Jung Archetype:  {t.get('jungian_archetype', '?')}\n"
                f"Mnemo Effect:    {t.get('mnemo_effect', '?')}\n"
                "----------------------------------\n"
            )
            self.triptych_text.insert(tk.END, info)
        else:
            self.triptych_text.insert(tk.END, "(no triptych loaded)")
        self.triptych_text.config(state=tk.DISABLED)

    def update_biases_display(self):
        self.biases_text.config(state=tk.NORMAL)
        self.biases_text.delete(1.0, tk.END)

        if not self.current_triptych:
            self.biases_text.insert(tk.END, "(no glyph)")
            self.biases_text.config(state=tk.DISABLED)
            return

        archetype = self.current_triptych.get('jungian_archetype', '').strip()
        active = CognitiveBiasOverlay.detect_active_biases(
            self.current_dna, self.palette_name, archetype, self.auto_mutate
        )

        self.biases_text.insert(tk.END, f"[ {len(active)} active biases ]\n\n")
        for bias in active:
            severity_marker = {"high": "!", "medium": "*", "low": "."}.get(bias['severity'], ".")
            self.biases_text.insert(tk.END, f"[{severity_marker}] {bias['name']}\n")
            self.biases_text.insert(tk.END, f"    {bias['description']}\n")
            self.biases_text.insert(tk.END, f"    -> {bias['mechanism']}\n\n")

        self.biases_text.config(state=tk.DISABLED)

    def update_philosophical_text(self):
        self.philo_text.config(state=tk.NORMAL)
        self.philo_text.delete(1.0, tk.END)
        self.philo_text.insert(tk.END, random.choice(PHILOSOPHICAL_STATEMENTS))
        self.philo_text.config(state=tk.DISABLED)

    def toggle_auto_mutate(self):
        """v7d : Correction du bug Tkinter"""
        self.auto_mutate = self.auto_var.get()
        if self.auto_mutate:
            self.start_auto_mutation()
        else:
            self.stop_auto_mutation()
        self.update_biases_display()

    def start_auto_mutation(self):
        def mutation_loop():
            while self.auto_var.get():
                self.after(0, self.mutate_current)
                import time
                time.sleep(3)
        if not self.mutation_thread or not self.mutation_thread.is_alive():
            self.mutation_thread = threading.Thread(target=mutation_loop, daemon=True)
            self.mutation_thread.start()

    def stop_auto_mutation(self):
        """v7d : Méthode correctement définie"""
        self.auto_mutate = False
        self.auto_var.set(False)

    def export_png(self):
        if not self.current_image:
            messagebox.showwarning("Export", "No glyph to export")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Image", "*.png")],
            initialfile=f"phobos_v7d_{abs(hash(self.current_dna.seed)) % 1000000:06d}.png"
        )
        if filename:
            img_4k, _ = HyperdimensionalGlyphGenerator.generate_glyph(
                width=3840, height=3840, dna=self.current_dna, palette_name=self.palette_name
            )
            if self.show_biases_var.get() and self.current_triptych:
                archetype = self.current_triptych.get('jungian_archetype', '').strip()
                active_biases = CognitiveBiasOverlay.detect_active_biases(
                    self.current_dna, self.palette_name, archetype, self.auto_mutate
                )
                img_4k = CognitiveBiasOverlay.render_bias_legend(img_4k, active_biases)
            img_4k.save(filename, "PNG", quality=100)
            messagebox.showinfo("Export", f"Glyph 4K saved:\n{filename}")

    def export_dna(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")],
            initialfile=f"dna_v7d_{abs(hash(self.current_dna.seed)) % 1000000:06d}.json"
        )
        if filename:
            dna_data = {
                "phobos_omega_version": "7d",
                "timestamp": datetime.now().isoformat(),
                "dna": {
                    "seed": self.current_dna.seed,
                    "complexity": self.current_dna.complexity,
                    "symmetry": self.current_dna.symmetry,
                    "resonance": self.current_dna.resonance,
                    "mutation_rate": self.current_dna.mutation_rate,
                    "dimensional_phase": self.current_dna.dimensional_phase,
                    "archetype_anchor": self.current_dna.archetype_anchor,
                    "triptych_id": self.current_dna.triptych_id
                },
                "palette": self.palette_name,
                "triptych": self.current_triptych,
                "active_biases": [b['name'] for b in CognitiveBiasOverlay.detect_active_biases(
                    self.current_dna, self.palette_name,
                    self.current_triptych.get('jungian_archetype', '').strip() if self.current_triptych else None,
                    self.auto_mutate
                )],
                "hash": abs(hash(self.current_dna.seed)) % 1000000
            }
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(dna_data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Export", f"DNA signature saved:\n{filename}")

    def export_flyer_v2(self):
        if not self.current_triptych:
            messagebox.showwarning("Export", "No active triptych")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Image", "*.png")],
            initialfile=f"flyer_v7d_{abs(hash(self.current_dna.seed)) % 1000000:06d}.png"
        )
        if filename:
            flyer = EnhancedMemeticFlyerGenerator.generate_archetypal_flyer(
                dna=self.current_dna,
                triptych=self.current_triptych,
                palette_name=self.palette_name,
                show_biases=self.show_biases_var.get(),
                auto_mutate=self.auto_mutate
            )
            flyer.save(filename, "PNG", quality=100)
            messagebox.showinfo("Export", f"Flyer V2 saved:\n{filename}")


# ====================== FLYER V2 (v7d - DejaVuSans + ASCII) ======================

class EnhancedMemeticFlyerGenerator:
    @staticmethod
    def _get_dejavu_font(size):
        """v7d : Force DejaVuSans (confirmé présent sur eLive)"""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "DejaVuSans-Bold.ttf",
        ]
        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except (IOError, OSError):
                continue
        return ImageFont.load_default()

    @staticmethod
    def generate_archetypal_flyer(dna, triptych, palette_name="phobos_classic",
                                  show_biases=False, auto_mutate=False):
        width, height = 1080, 1920
        img = Image.new('RGB', (width, height), (10, 10, 26))
        draw = ImageDraw.Draw(img, 'RGBA')

        # Glyphe
        glyph_img, _ = HyperdimensionalGlyphGenerator.generate_glyph(
            width=800, height=800, dna=dna, palette_name=palette_name
        )

        if show_biases:
            archetype = triptych.get('jungian_archetype', '').strip()
            active_biases = CognitiveBiasOverlay.detect_active_biases(
                dna, palette_name, archetype, auto_mutate
            )
            glyph_img = CognitiveBiasOverlay.render_bias_legend(glyph_img, active_biases)

        img.paste(glyph_img, (140, 300), glyph_img)

        # v7d : DejaVuSans partout
        title_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(72)
        text_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(36)
        small_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(24)
        symbol_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(48)
        tiny_font = EnhancedMemeticFlyerGenerator._get_dejavu_font(18)

        # v7d : TOUT EN ASCII
        von_p = triptych.get('von_petzinger', '?')
        futh = triptych.get('futhark', '?')
        von_p_safe = safe_symbol(von_p, VON_PETZINGER_ASCII)
        futh_safe = safe_symbol(futh, FUTHARK_ASCII)

        draw.text((width//2, 120), to_ascii("PHOBOS-OMEGA v7d"), fill="#ff0066",
                  font=title_font, anchor="mm")
        draw.text((width//2, 220), von_p_safe, fill="#00ffaa",
                  font=symbol_font, anchor="mm")
        draw.text((width//2, 320), f"[ {futh_safe} ]", fill="#ffaa00",
                  font=text_font, anchor="mm")

        archetype = triptych.get('jungian_archetype', '').strip()
        effect = triptych.get('mnemo_effect', '').strip()
        draw.text((width//2, 1200), to_ascii(archetype), fill="#ccccff",
                  font=text_font, anchor="mm")
        draw.text((width//2, 1260), f"[ {to_ascii(effect)} ]", fill="#00ffaa",
                  font=small_font, anchor="mm")

        draw.text((width//2, 1350), f"DNA: {abs(hash(dna.seed)) % 1000000:06d}",
                  fill="#6666aa", font=small_font, anchor="mm")

        msg = random.choice(PHILOSOPHICAL_STATEMENTS).split('\n')[0]
        draw.text((width//2, 1420), to_ascii(msg), fill="#88ccff",
                  font=small_font, anchor="mm")

        draw.text((width//2, height-80),
                  "[ Zero Hazard - Full Spectrum - Meta-Stable - Biased ]",
                  fill="#444466", font=tiny_font, anchor="mm")

        return img


# ====================== POINT D'ENTRÉE ======================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lexicon_path = os.path.join(script_dir, "paleo_mnemos_lexicon.json")

    app = PhobosOmegaV7d(lexicon_path=lexicon_path)
    print("=" * 60)
    print("  PHOBOS-OMEGA v7d - Paleo-Mnemos Memetic Engine")
    print("=" * 60)
    print("  [ Zero Hazard Architecture ]")
    print("  [ Full Spectrum Palette System ]")
    print("  [ DNA-Based Mutation Engine ]")
    print("  [ Paleo-Mnemos Lexicon Integration ]")
    print("  [ 20 Cognitive Biases Overlay ]")
    print("  [ Enhanced Memetic Flyer V2 ]")
    print("  [ ASCII-Only Mode for eLive ]")
    print("  [ DejaVuSans Priority Fonts ]")
    print("=" * 60)
    print()
    app.mainloop()


if __name__ == "__main__":
    main()

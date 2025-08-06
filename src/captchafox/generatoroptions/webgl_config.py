import random

from typing import Tuple, Dict, Any


WEBGL_CONFIG = {
    "windows": {
        "Google Inc. (NVIDIA)": {
            "weight": 0.503,
            "renders": {
                "ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0), or similar": 0.497,
                "ANGLE (NVIDIA, NVIDIA GeForce 8800 GTX Direct3D11 vs_4_0 ps_4_0)": 0.002,
                "ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0)": 0.002,
                "ANGLE (NVIDIA, NVIDIA GeForce GTX 480 Direct3D11 vs_5_0 ps_5_0)": 0.002,
            },
        },
        "Google Inc. (Intel)": {
            "weight": 0.458,
            "renders": {
                "ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0), or similar": 0.241,
                "ANGLE (Intel, Intel(R) HD Graphics 400 Direct3D11 vs_5_0 ps_5_0), or similar": 0.197,
                "ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0)": 0.009,
                "ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_4_1 ps_4_1), or similar": 0.005,
                "ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_4_0 ps_4_0)": 0.002,
                "ANGLE (Intel, Intel 945GM Direct3D11 vs_4_0 ps_4_0)": 0.002,
                "ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_4_1 ps_4_1)": 0.002,
            },
        },
        "Google Inc. (AMD)": {
            "weight": 0.1388,
            "renders": {
                "ANGLE (AMD, Radeon HD 3200 Graphics Direct3D11 vs_5_0 ps_5_0), or similar": 0.0106,
                "ANGLE (AMD, Radeon R9 200 Series Direct3D11 vs_5_0 ps_5_0), or similar": 0.066,
                "ANGLE (AMD, Radeon R9 200 Series Direct3D11 vs_5_0 ps_5_0)": 0.002,
            },
        },
        "Google Inc. (Microsoft)": {
            "weight": 0.0128,
            "renders": {"ANGLE (Microsoft, Microsoft Basic Render Driver Direct3D11 vs_5_0 ps_5_0), or similar": 0.016},
        },
        "Google Inc. (Google)": {
            "weight": 0.0024,
            "renders": {"ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)": 0.003},
        },
    },
    "macos": {
        "Apple": {"weight": 0.8439, "renders": {"Apple M1, or similar": 0.8439}},
        "Intel Inc.": {
            "weight": 0.1099,
            "renders": {"Intel(R) HD Graphics 400, or similar": 0.0760, "Intel(R) HD Graphics, or similar": 0.0339},
        },
        "ATI Technologies Inc.": {"weight": 0.0380, "renders": {"Radeon R9 200 Series, or similar": 0.0380}},
        "Google Inc. (NVIDIA)": {
            "weight": 0.0082,
            "renders": {"ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0), or similar": 0.0082},
        },
    },
    "linux": {
        "Intel": {
            "weight": 0.4559,
            "renders": {
                "Intel(R) HD Graphics, or similar": 0.2823,
                "Intel(R) HD Graphics 400, or similar": 0.1540,
                "Intel(R) HD Graphics 400": 0.0195,
            },
        },
        "NVIDIA Corporation": {
            "weight": 0.2628,
            "renders": {"NVIDIA GeForce GTX 980, or similar": 0.2567, "NVIDIA GeForce GTX 980/PCIe/SSE2": 0.0062},
        },
        "AMD": {
            "weight": 0.1858,
            "renders": {"Radeon R9 200 Series, or similar": 0.1027, "Radeon HD 3200 Graphics, or similar": 0.0832},
        },
        "Mesa": {
            "weight": 0.0832,
            "renders": {"llvmpipe, or similar": 0.0575, "llvmpipe": 0.0195, "GeForce GTX 980, or similar": 0.0062},
        },
        "Mesa/X.org": {"weight": 0.0123, "renders": {"llvmpipe, or similar": 0.0123}},
    },
}


def generate_webgl_config(launch_options: Dict[str, Any]) -> Tuple[str, str]:
    "Случайный WebGL config"
    configs = WEBGL_CONFIG[launch_options["os"]]

    venders = list(configs.keys())
    ps = [weight["weight"] for weight in configs.values()]

    vender = random.choices(venders, weights=ps, k=1)[0]  # type: ignore
    configs_vender = configs[vender]["renders"]

    renders = list(configs_vender.keys())
    ps = list(configs_vender.values())

    render = random.choices(renders, weights=ps, k=1)[0]

    return vender, render

const { GoogleGenAI } = require("@google/genai");
const fs = require("node:fs");
const path = require("node:path");

// Load .env file from project root
function loadEnv() {
  const possiblePaths = [
    path.join(__dirname, "../../.env"),
    path.join(__dirname, "../.env"),
    path.join(process.cwd(), ".env"),
  ];

  for (const envPath of possiblePaths) {
    if (fs.existsSync(envPath)) {
      const envContent = fs.readFileSync(envPath, "utf-8");
      envContent.split("\n").forEach((line) => {
        const [key, value] = line.split("=");
        if (key && value) {
          process.env[key.trim()] = value.trim();
        }
      });
      return true;
    }
  }
  return false;
}

/**
 * Generate an image using Gemini API
 * @param {string} prompt - The image generation prompt
 * @param {string} outputPath - Where to save the generated image
 * @param {object} options - Optional settings
 * @returns {Promise<{success: boolean, path?: string, text?: string, error?: string}>}
 */
async function generateImage(prompt, outputPath, options = {}) {
  loadEnv();

  const apiKey = process.env.GOOGLE_API_KEY;
  if (!apiKey) {
    return {
      success: false,
      error: "GOOGLE_API_KEY not found. Add it to .env file."
    };
  }

  const ai = new GoogleGenAI({ apiKey });
  const model = options.model || "gemini-2.0-flash-exp-image-generation";

  try {
    const response = await ai.models.generateContent({
      model,
      contents: prompt,
      config: {
        responseModalities: ["Text", "Image"],
      },
    });

    let textResponse = "";
    let imageSaved = false;

    for (const part of response.candidates[0].content.parts) {
      if (part.text) {
        textResponse = part.text;
      } else if (part.inlineData) {
        const imageData = part.inlineData.data;
        const buffer = Buffer.from(imageData, "base64");
        fs.writeFileSync(outputPath, buffer);
        imageSaved = true;
      }
    }

    if (imageSaved) {
      return { success: true, path: outputPath, text: textResponse };
    } else {
      return { success: false, error: "No image was generated", text: textResponse };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Generate a slide background image
 * @param {string} theme - Description of the slide theme/content
 * @param {string} outputPath - Where to save the image
 * @param {object} colors - Color scheme { primary, accent1, accent2, background }
 */
async function generateSlideBackground(theme, outputPath, colors = {}) {
  const {
    background = "#0f0f1a",
    primary = "#667eea",
    accent1 = "#00d4ff",
    accent2 = "#764ba2",
  } = colors;

  const prompt = `Create an abstract futuristic background image for a presentation slide.
Theme: ${theme}
Style: Dark theme with ${background} background color.
Elements: Abstract flowing digital elements, subtle geometric patterns, particles of light.
Color accents: Use hints of ${primary}, ${accent1}, and ${accent2}.
Mood: Professional, modern technology, clean and elegant.
The image should be subtle enough to work as a background with text overlaid on top.
Dimensions: Wide format suitable for a 16:9 presentation slide.
No text, logos, or words in the image.`;

  return generateImage(prompt, outputPath);
}

/**
 * Generate an icon/illustration for a slide
 * @param {string} concept - What the icon should represent
 * @param {string} outputPath - Where to save the image
 * @param {string} style - Style description (e.g., "minimalist", "3d", "flat")
 */
async function generateIcon(concept, outputPath, style = "minimalist") {
  const prompt = `Create a ${style} icon representing: ${concept}.
Style: Clean, professional, suitable for a business presentation.
Background: Transparent or dark (#0f0f1a).
Colors: Use blues (#667eea, #00d4ff) and purples (#764ba2) on dark background.
Size: Square format, simple and recognizable.
No text in the image.`;

  return generateImage(prompt, outputPath);
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.log(`Usage: node generate-image.js <type> <output> [options]

Types:
  background <output> "<theme>"     - Generate slide background
  icon <output> "<concept>"         - Generate icon/illustration
  custom <output> "<prompt>"        - Custom prompt

Examples:
  node generate-image.js background bg.png "digital payments and blockchain"
  node generate-image.js icon payment-icon.png "secure digital transaction"
  node generate-image.js custom hero.png "futuristic city with glowing networks"
`);
    process.exit(1);
  }

  const [type, output, ...rest] = args;
  const text = rest.join(" ");

  async function run() {
    let result;

    switch (type) {
      case "background":
        console.log(`Generating background for: "${text}"`);
        result = await generateSlideBackground(text, output);
        break;
      case "icon":
        console.log(`Generating icon for: "${text}"`);
        result = await generateIcon(text, output);
        break;
      case "custom":
        console.log(`Generating with custom prompt: "${text}"`);
        result = await generateImage(text, output);
        break;
      default:
        console.error(`Unknown type: ${type}`);
        process.exit(1);
    }

    if (result.success) {
      console.log(`Image saved to: ${result.path}`);
      if (result.text) {
        console.log(`AI response: ${result.text}`);
      }
    } else {
      console.error(`Error: ${result.error}`);
      if (result.text) {
        console.log(`AI response: ${result.text}`);
      }
      process.exit(1);
    }
  }

  run();
}

module.exports = { generateImage, generateSlideBackground, generateIcon };

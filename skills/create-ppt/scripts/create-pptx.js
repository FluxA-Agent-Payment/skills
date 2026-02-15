/**
 * Convert HTML slides to PowerPoint presentation
 */

const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');
const path = require('path');
const fs = require('fs');

async function createPresentation() {
    const pptx = new pptxgen();

    // Set presentation properties
    pptx.layout = 'LAYOUT_16x9';
    pptx.title = 'x402 - Internet-Native Payments Standard';
    pptx.author = 'x402 Protocol';
    pptx.subject = 'x402 Protocol Overview and V2 Features';

    // Get all slide files in order
    const slidesDir = path.join(__dirname, '..', 'slides');
    const slideFiles = fs.readdirSync(slidesDir)
        .filter(f => f.endsWith('.html'))
        .sort();

    console.log(`Found ${slideFiles.length} slides to convert...`);

    // Convert each slide
    for (const slideFile of slideFiles) {
        const slidePath = path.join(slidesDir, slideFile);
        console.log(`Converting: ${slideFile}`);

        try {
            await html2pptx(slidePath, pptx);
            console.log(`  Done: ${slideFile}`);
        } catch (error) {
            console.error(`  Error converting ${slideFile}:`, error.message);
            // Continue with other slides
        }
    }

    // Save the presentation
    const outputPath = path.join(__dirname, '..', 'x402_presentation_v2.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`\nPresentation saved to: ${outputPath}`);
}

createPresentation().catch(console.error);

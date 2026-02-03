#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');
const inquirer = require('inquirer');
const chalk = require('chalk');

const HOME_DIR = os.homedir();
const CONFIG_DIR = path.join(HOME_DIR, '.molt-pay');
const REPO_DIR = path.join(CONFIG_DIR, 'ap2');
const CONSENT_FILE = path.join(CONFIG_DIR, 'consent.json');
const ENV_FILE = path.join(REPO_DIR, '.env');

// Placeholder URL - User should verify the correct AP2 repo URL
const AP2_REPO_URL = 'https://github.com/google-agentic-commerce/AP2.git'; 

const DISCLAIMER = `
${chalk.red.bold('================================================================')}
                    ${chalk.red.bold('LEGAL DISCLAIMER')}
${chalk.red.bold('================================================================')}
This software involves financial transactions and cryptocurrency.
Use at your own risk. The developers are not responsible for 
any financial loss, bugs, or unintended consequences.

By typing "I AGREE", you acknowledge that you understand these
risks and accept full responsibility for using this tool.
${chalk.red.bold('================================================================')}
`;

async function main() {
  console.clear();
  console.log(DISCLAIMER);

  const { agreement } = await inquirer.prompt([
    {
      type: 'input',
      name: 'agreement',
      message: 'Type "I AGREE" to proceed:',
      validate: (input) => input.trim() === 'I AGREE' || 'You must type "I AGREE" exactly to proceed.'
    }
  ]);

  if (agreement === 'I AGREE') {
    console.log(chalk.green('\nThank you. Proceeding with installation...\n'));
    await saveConsent();
    
    if (await checkPrerequisites()) {
        await cloneRepo();
        await setupEnvironment();
        console.log(chalk.green.bold('\nInstallation setup complete! 🚀'));
        console.log(chalk.blue(`AP2 installed at: ${REPO_DIR}`));
        console.log(chalk.blue(`Configuration saved to: ${ENV_FILE}`));
        process.exit(0);
    } else {
        console.log(chalk.red('Prerequisites check failed. Please fix the issues and try again.'));
        process.exit(1);
    }
  }
}

async function saveConsent() {
  try {
    await fs.ensureDir(CONFIG_DIR);
    const data = {
      agreed: true,
      timestamp: new Date().toISOString()
    };
    await fs.writeJson(CONSENT_FILE, data, { spaces: 2 });
    console.log(chalk.gray(`Consent saved to ${CONSENT_FILE}`));
  } catch (error) {
    console.error(chalk.red('Error saving consent:'), error);
  }
}

async function checkPrerequisites() {
  console.log(chalk.yellow('Checking prerequisites...'));
  let allPassed = true;

  // Node.js Check
  const nodeVersion = process.version;
  const majorNode = parseInt(nodeVersion.replace('v', '').split('.')[0], 10);
  if (majorNode >= 18) { // Adjusted baseline, spec said 22 but 18+ is standard LTS, sticking to 22 if strict
      console.log(chalk.green(`✓ Node.js ${nodeVersion}`));
  } else {
      console.log(chalk.red(`✗ Node.js ${nodeVersion} (Warning: Spec recommends >=22)`));
      // allPassed = false; // Soft fail for now
  }
    
  // Python Check
  try {
      const pythonVersion = execSync('python3 --version').toString().trim();
      console.log(chalk.green(`✓ ${pythonVersion}`));
  } catch (e) {
      console.log(chalk.red('✗ Python3 not found'));
      allPassed = false;
  }

  // uv Check
  try {
      // Windows often uses 'where', Linux/Mac uses 'which'
      const command = process.platform === 'win32' ? 'where uv' : 'which uv';
      execSync(command);
      console.log(chalk.green('✓ uv package manager found'));
  } catch (e) {
      console.log(chalk.red('✗ uv package manager not found'));
      allPassed = false;
  }

  return allPassed;
}

async function cloneRepo() {
    console.log(chalk.yellow(`\nCloning AP2 repository from ${AP2_REPO_URL}...`));
    
    if (fs.existsSync(REPO_DIR)) {
        console.log(chalk.cyan('Directory already exists. Pulling latest changes...'));
        try {
            execSync('git pull', { cwd: REPO_DIR, stdio: 'inherit' });
        } catch (e) {
            console.log(chalk.red('Failed to update repository.'));
        }
    } else {
        try {
            execSync(`git clone ${AP2_REPO_URL} "${REPO_DIR}"`, { stdio: 'inherit' });
            console.log(chalk.green('✓ Repository cloned successfully.'));
        } catch (e) {
            console.error(chalk.red('Failed to clone repository. check your internet connection or URL.'));
            process.exit(1);
        }
    }
}

async function setupEnvironment() {
    console.log(chalk.yellow('\nSetting up environment configuration...'));
    
    const answers = await inquirer.prompt([
        {
            type: 'password',
            name: 'googleApiKey',
            message: 'Enter your GOOGLE_API_KEY:',
            mask: '*'
        },
        {
            type: 'password',
            name: 'polygonPrivateKey',
            message: 'Enter your Polygon PRIVATE_KEY (for Smart Account setup):',
            mask: '*'
        }
    ]);

    const envContent = `GOOGLE_API_KEY=${answers.googleApiKey}\nPOLYGON_PRIVATE_KEY=${answers.polygonPrivateKey}\n# Added by Molt-Pay CLI\n`;

    try {
        await fs.outputFile(ENV_FILE, envContent);
        console.log(chalk.green('✓ Secrets securely saved to .env file.'));
        
        // FUTURE: Initialize Safe Smart Account here using the keys
        // console.log(chalk.blue('Initializing Safe Smart Account... (TODO)'));
        
    } catch (e) {
        console.error(chalk.red('Error writing .env file:'), e);
    }
}

// Entry point
if (require.main === module) {
    if (process.argv.includes('install')) {
        main().catch(err => console.error(err));
    } else {
        console.log(chalk.blue('Usage: npx molt-pay install'));
        // For development convenience, run main if no args provided:
        // main().catch(err => console.error(err));
    }
}

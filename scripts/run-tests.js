#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

function log(message, color = colors.reset) {
  console.log(`${color}${message}${colors.reset}`);
}

function runCommand(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      stdio: 'inherit',
      shell: true,
      ...options,
    });

    child.on('close', (code) => {
      if (code === 0) {
        resolve(code);
      } else {
        reject(new Error(`Command failed with exit code ${code}`));
      }
    });

    child.on('error', (error) => {
      reject(error);
    });
  });
}

async function runTests() {
  log('\n🧪 Running Brand Audit Tool Test Suite', colors.bright + colors.cyan);
  log('=' * 50, colors.cyan);

  const testSuites = [
    {
      name: 'Unit Tests',
      command: 'npm',
      args: ['run', 'test', '--', '--coverage', '--watchAll=false'],
      description: 'Testing utilities, services, and components',
    },
    {
      name: 'Type Checking',
      command: 'npm',
      args: ['run', 'type-check'],
      description: 'Checking TypeScript types',
    },
    {
      name: 'Linting',
      command: 'npm',
      args: ['run', 'lint'],
      description: 'Checking code quality and style',
    },
    {
      name: 'Build Test',
      command: 'npm',
      args: ['run', 'build'],
      description: 'Testing production build',
    },
  ];

  const results = [];

  for (const suite of testSuites) {
    log(`\n📋 Running ${suite.name}...`, colors.bright + colors.blue);
    log(`   ${suite.description}`, colors.blue);
    
    const startTime = Date.now();
    
    try {
      await runCommand(suite.command, suite.args);
      const duration = Date.now() - startTime;
      
      log(`✅ ${suite.name} passed (${duration}ms)`, colors.green);
      results.push({ name: suite.name, status: 'passed', duration });
    } catch (error) {
      const duration = Date.now() - startTime;
      
      log(`❌ ${suite.name} failed (${duration}ms)`, colors.red);
      log(`   Error: ${error.message}`, colors.red);
      results.push({ name: suite.name, status: 'failed', duration, error: error.message });
    }
  }

  // Summary
  log('\n📊 Test Results Summary', colors.bright + colors.magenta);
  log('=' * 30, colors.magenta);

  const passed = results.filter(r => r.status === 'passed').length;
  const failed = results.filter(r => r.status === 'failed').length;
  const total = results.length;

  results.forEach(result => {
    const icon = result.status === 'passed' ? '✅' : '❌';
    const color = result.status === 'passed' ? colors.green : colors.red;
    log(`${icon} ${result.name} (${result.duration}ms)`, color);
    
    if (result.error) {
      log(`   ${result.error}`, colors.red);
    }
  });

  log(`\n📈 Overall: ${passed}/${total} test suites passed`, 
    failed === 0 ? colors.green : colors.yellow);

  if (failed > 0) {
    log(`\n⚠️  ${failed} test suite(s) failed. Please check the output above.`, colors.red);
    process.exit(1);
  } else {
    log('\n🎉 All test suites passed!', colors.green);
  }
}

// E2E Tests (separate function as they require the server to be running)
async function runE2ETests() {
  log('\n🌐 Running End-to-End Tests', colors.bright + colors.cyan);
  log('Note: Make sure the development server is running on port 3002', colors.yellow);
  
  try {
    await runCommand('npx', ['playwright', 'test']);
    log('✅ E2E tests passed', colors.green);
  } catch (error) {
    log('❌ E2E tests failed', colors.red);
    log(`   Error: ${error.message}`, colors.red);
    log('\n💡 Tips for E2E test failures:', colors.yellow);
    log('   - Ensure the dev server is running: npm run dev', colors.yellow);
    log('   - Check if the database is properly set up', colors.yellow);
    log('   - Verify environment variables are configured', colors.yellow);
  }
}

// Performance Tests
async function runPerformanceTests() {
  log('\n⚡ Running Performance Tests', colors.bright + colors.cyan);
  
  try {
    await runCommand('npm', ['run', 'test', '--', '--testPathPattern=performance', '--watchAll=false']);
    log('✅ Performance tests passed', colors.green);
  } catch (error) {
    log('❌ Performance tests failed', colors.red);
    log(`   Error: ${error.message}`, colors.red);
  }
}

// Main execution
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    log('Brand Audit Tool Test Runner', colors.bright);
    log('\nUsage: node scripts/run-tests.js [options]', colors.cyan);
    log('\nOptions:', colors.cyan);
    log('  --unit          Run only unit tests', colors.cyan);
    log('  --e2e           Run only E2E tests', colors.cyan);
    log('  --performance   Run only performance tests', colors.cyan);
    log('  --all           Run all tests (default)', colors.cyan);
    log('  --help, -h      Show this help message', colors.cyan);
    return;
  }

  try {
    if (args.includes('--unit')) {
      await runTests();
    } else if (args.includes('--e2e')) {
      await runE2ETests();
    } else if (args.includes('--performance')) {
      await runPerformanceTests();
    } else {
      // Run all tests by default
      await runTests();
      
      if (args.includes('--all')) {
        await runPerformanceTests();
        
        log('\n🤖 To run E2E tests, start the dev server and run:', colors.yellow);
        log('   npm run dev (in another terminal)', colors.yellow);
        log('   node scripts/run-tests.js --e2e', colors.yellow);
      }
    }
  } catch (error) {
    log(`\n💥 Test runner failed: ${error.message}`, colors.red);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { runTests, runE2ETests, runPerformanceTests };

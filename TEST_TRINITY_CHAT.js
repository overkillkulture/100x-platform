// Trinity Command Chat - Automated Testing Script
// Run this in browser console while Trinity Command Chat is open

console.log('🔧 C1 MECHANIC - TRINITY CHAT TESTING INITIATED');
console.log('================================================\n');

// Test Results Storage
const testResults = {
    passed: [],
    failed: [],
    warnings: []
};

function log(status, test, details) {
    const result = `[${status}] ${test}${details ? ': ' + details : ''}`;
    console.log(result);
    if (status === '✅') testResults.passed.push(test);
    if (status === '❌') testResults.failed.push(test);
    if (status === '⚠️') testResults.warnings.push(test);
}

// TEST 1: Agent Selection
console.log('\n📋 TEST 1: AGENT SELECTION');
try {
    selectAgent('C1');
    if (currentAgent === 'C1') {
        log('✅', 'C1 Agent Selection', 'Successfully set to C1');
    } else {
        log('❌', 'C1 Agent Selection', `Expected C1, got ${currentAgent}`);
    }
} catch(e) {
    log('❌', 'C1 Agent Selection', e.message);
}

// TEST 2: Send Message
console.log('\n📋 TEST 2: SEND MESSAGE');
try {
    const initialMsgCount = messages.length;
    document.getElementById('message-input').value = 'C1 Mechanic reporting for duty - testing communications';
    sendMessage();
    if (messages.length === initialMsgCount + 1) {
        log('✅', 'Send Message', 'Message added to history');
    } else {
        log('❌', 'Send Message', 'Message not added');
    }
} catch(e) {
    log('❌', 'Send Message', e.message);
}

// TEST 3: Command - /status
console.log('\n📋 TEST 3: COMMAND /status');
try {
    const beforeCount = messages.length;
    document.getElementById('message-input').value = '/status';
    sendMessage();
    if (messages.length > beforeCount) {
        log('✅', '/status Command', 'System message generated');
    } else {
        log('❌', '/status Command', 'No response');
    }
} catch(e) {
    log('❌', '/status Command', e.message);
}

// TEST 4: Command - /help
console.log('\n📋 TEST 4: COMMAND /help');
try {
    const beforeCount = messages.length;
    document.getElementById('message-input').value = '/help';
    sendMessage();
    if (messages.length > beforeCount) {
        log('✅', '/help Command', 'Help message displayed');
    } else {
        log('❌', '/help Command', 'No response');
    }
} catch(e) {
    log('❌', '/help Command', e.message);
}

// TEST 5: Task Creation
console.log('\n📋 TEST 5: TASK CREATION');
try {
    const initialTaskCount = tasks.length;
    document.getElementById('task-title').value = 'Test the login flow';
    document.getElementById('task-assign').value = 'C1';
    createTask();
    if (tasks.length === initialTaskCount + 1) {
        log('✅', 'Task Creation', 'Task successfully created');
    } else {
        log('❌', 'Task Creation', 'Task not added');
    }
} catch(e) {
    log('❌', 'Task Creation', e.message);
}

// TEST 6: Task Completion Toggle
console.log('\n📋 TEST 6: TASK COMPLETION');
try {
    const testTask = tasks[tasks.length - 1];
    const wasCompleted = testTask.completed;
    toggleTask(testTask.id);
    if (testTask.completed !== wasCompleted) {
        log('✅', 'Task Toggle', 'Task completion toggled successfully');
    } else {
        log('❌', 'Task Toggle', 'Task state did not change');
    }
} catch(e) {
    log('❌', 'Task Toggle', e.message);
}

// TEST 7: Tab Switching
console.log('\n📋 TEST 7: TAB SWITCHING');
try {
    const agentsTab = document.querySelectorAll('.tab')[0];
    const tasksTab = document.querySelectorAll('.tab')[1];

    tasksTab.click();
    if (currentTab === 'tasks') {
        log('✅', 'Switch to Tasks Tab', 'Successfully switched');
    } else {
        log('❌', 'Switch to Tasks Tab', 'Tab did not switch');
    }

    agentsTab.click();
    if (currentTab === 'agents') {
        log('✅', 'Switch to Agents Tab', 'Successfully switched');
    } else {
        log('❌', 'Switch to Agents Tab', 'Tab did not switch');
    }
} catch(e) {
    log('❌', 'Tab Switching', e.message);
}

// TEST 8: Agent Status Display
console.log('\n📋 TEST 8: AGENT STATUS DISPLAY');
try {
    switchTab('agents');
    const agentCards = document.querySelectorAll('.agent-card');
    if (agentCards.length === 4) {
        log('✅', 'Agent Display', 'All 4 agents shown');
    } else {
        log('⚠️', 'Agent Display', `Expected 4, found ${agentCards.length}`);
    }

    const c1Card = Array.from(agentCards).find(card => card.textContent.includes('C1'));
    if (c1Card && c1Card.classList.contains('online')) {
        log('✅', 'C1 Online Status', 'C1 marked as online');
    } else {
        log('❌', 'C1 Online Status', 'C1 not marked online');
    }
} catch(e) {
    log('❌', 'Agent Status Display', e.message);
}

// TEST 9: LocalStorage Persistence
console.log('\n📋 TEST 9: LOCALSTORAGE PERSISTENCE');
try {
    const storedMessages = localStorage.getItem('trinity_messages');
    const storedStatus = localStorage.getItem('trinity_agent_status');
    const storedTasks = localStorage.getItem('trinity_tasks');

    if (storedMessages) log('✅', 'Messages Persistence', 'Messages stored');
    else log('❌', 'Messages Persistence', 'No messages in storage');

    if (storedStatus) log('✅', 'Agent Status Persistence', 'Status stored');
    else log('❌', 'Agent Status Persistence', 'No status in storage');

    if (storedTasks) log('✅', 'Tasks Persistence', 'Tasks stored');
    else log('❌', 'Tasks Persistence', 'No tasks in storage');
} catch(e) {
    log('❌', 'LocalStorage Persistence', e.message);
}

// TEST 10: Quick Command Buttons
console.log('\n📋 TEST 10: QUICK COMMAND BUTTONS');
try {
    const quickCmds = document.querySelectorAll('.quick-cmd');
    if (quickCmds.length === 4) {
        log('✅', 'Quick Commands Display', 'All 4 buttons shown');
    } else {
        log('⚠️', 'Quick Commands Display', `Expected 4, found ${quickCmds.length}`);
    }

    // Test clicking one
    quickCmds[0].click();
    const inputValue = document.getElementById('message-input').value;
    if (inputValue.startsWith('/')) {
        log('✅', 'Quick Command Click', 'Command inserted into input');
    } else {
        log('❌', 'Quick Command Click', 'Command not inserted');
    }
} catch(e) {
    log('❌', 'Quick Command Buttons', e.message);
}

// SUMMARY
console.log('\n\n================================================');
console.log('🔧 C1 MECHANIC - TEST SUMMARY');
console.log('================================================');
console.log(`✅ PASSED: ${testResults.passed.length}`);
console.log(`❌ FAILED: ${testResults.failed.length}`);
console.log(`⚠️ WARNINGS: ${testResults.warnings.length}`);
console.log('\nDETAILS:');
if (testResults.failed.length > 0) {
    console.log('\n❌ FAILED TESTS:');
    testResults.failed.forEach(t => console.log('  - ' + t));
}
if (testResults.warnings.length > 0) {
    console.log('\n⚠️ WARNINGS:');
    testResults.warnings.forEach(t => console.log('  - ' + t));
}
console.log('\n✅ PASSED TESTS:');
testResults.passed.forEach(t => console.log('  - ' + t));

console.log('\n\n🔧 C1 RECOMMENDATIONS GENERATING...');

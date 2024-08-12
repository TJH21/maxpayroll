// navigation/MainStackNavigator.js
import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';

// Import your screens
import EmployeeListScreen from '../screens/EmployeeListScreen';
import EmployeeDetailScreen from '../screens/EmployeeDetailScreen';
import PayrollProcessingScreen from '../screens/PayrollProcessingScreen';

const Stack = createStackNavigator();

const MainStackNavigator = () => {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="EmployeeList">
                <Stack.Screen name="EmployeeList" component={EmployeeListScreen} options={{ title: 'Employees' }} />
                <Stack.Screen name="EmployeeDetail" component={EmployeeDetailScreen} options={{ title: 'Employee Details' }} />
                <Stack.Screen name="PayrollProcessing" component={PayrollProcessingScreen} options={{ title: 'Payroll Processing' }} />
            </Stack.Navigator>
        </NavigationContainer>
    );
};

export default MainStackNavigator;

// screens/PayrollProcessingScreen.js
import React, { useState } from 'react';
import { View, Text, Button, Alert, StyleSheet } from 'react-native';
import axios from 'axios';

const PayrollProcessingScreen = ({ route }) => {
    const { employeeId } = route.params;

    const processPayroll = () => {
        axios.post(`http://localhost:8000/api/employees/${employeeId}/process_payroll/`)
            .then(response => {
                Alert.alert('Payroll Processed', `Net Pay: £${response.data.net_pay}`);
            })
            .catch(error => {
                console.error(error);
                Alert.alert('Error', 'Failed to process payroll.');
            });
    };

    return (
        <View style={styles.container}>
            <Text style={styles.infoText}>Process payroll for the selected employee.</Text>
            <Button title="Process Payroll" onPress={processPayroll} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 16,
        backgroundColor: '#f8f8f8',
    },
    infoText: {
        fontSize: 16,
        marginBottom: 16,
    },
});

export default PayrollProcessingScreen;

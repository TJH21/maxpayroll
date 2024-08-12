// screens/EmployeeDetailScreen.js
import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import axios from 'axios';

const EmployeeDetailScreen = ({ route }) => {
    const { employeeId } = route.params;
    const [employee, setEmployee] = useState(null);

    useEffect(() => {
        // Fetch the employee details from the API
        axios.get(`http://localhost:8000/api/employees/${employeeId}/`)
            .then(response => setEmployee(response.data))
            .catch(error => console.error(error));
    }, [employeeId]);

    if (!employee) {
        return (
            <View style={styles.container}>
                <Text>Loading...</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <Text style={styles.label}>Name:</Text>
            <Text style={styles.value}>{employee.first_name} {employee.last_name}</Text>

            <Text style={styles.label}>Department:</Text>
            <Text style={styles.value}>{employee.department.name}</Text>

            <Text style={styles.label}>Date of Birth:</Text>
            <Text style={styles.value}>{employee.dob}</Text>

            <Text style={styles.label}>Salary:</Text>
            <Text style={styles.value}>£{employee.salary}</Text>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 16,
        backgroundColor: '#f8f8f8',
    },
    label: {
        fontSize: 16,
        fontWeight: 'bold',
        marginTop: 16,
    },
    value: {
        fontSize: 16,
        marginBottom: 16,
    },
});

export default EmployeeDetailScreen;
